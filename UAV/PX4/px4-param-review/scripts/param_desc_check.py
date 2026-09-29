#!/usr/bin/env python3
"""Mechanical checks for PX4 parameter descriptions changed between two git refs.

Read-only against the clone: it reads files with `git show` (or from the working
tree), writes nothing into the clone, and runs the project's own YAML schema
validator on copies of the head files placed in a scratch directory.

Usage:
  param_desc_check.py --repo <clone> --base <ref> --head <ref|WORKTREE> \
      --scratch <dir> [--all] <file.yaml> [...]

Prints, per changed parameter: its classification (new, rewritten,
metadata-only, removed), line numbers in the head file, description sizes
before and after, and candidate flags for the lenses to confirm. Ends with
size totals and the validator's output.

--all audits every parameter in the named files as if new (no diff).
"""

import argparse
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip3 install --user pyyaml")

SHORT_MAX = 70  # validation/module_schema.yaml

BOILERPLATE = [
    r"\bThis parameter\b", r"\bThis param\b", r"\bNote that\b", r"\bNote:", r"\bPlease\b",
    r"\bis used to\b", r"\ballows? (?:you )?to\b", r"\bIn other words\b",
    r"\bIt is recommended\b", r"\bbasically\b", r"\bsimply\b",
]
SYMBOL_WORDS = [r"<=", r">=", r"[²³]", r"\s&\s", r"\s->\s", r"=>"]
# Non-stock wording for ideas the standard has a stock phrase for.
STOCK_VARIANTS = [
    (r"\b(?:set (?:this|the) (?:parameter|value) to|a value of|setting (?:it|this) to) (?:zero|0)\b[^.]*\b(?:disables?|turns? off)",
     "Set to 0 to disable."),
    (r"\b(?:zero|0) (?:disables|turns off)\b", "Set to 0 to disable."),
    (r"\b(?:a value of|set (?:this|the) (?:parameter|value) to) -1\b[^.]*\b(?:disables?|turns? off)", "Set to -1 to disable."),
    (r"\bonly (?:relevant|applies|valid|active|effective) (?:if|when|in)\b|\bonly used (?:if|in)\b", "Only used when X is enabled."),
    (r"\bfor example\b", "e.g."),
    (r"\beg\b|\be\.g\b(?!\.)", "e.g."),
]
UNIT_WORDS = r"\b(?:in|expressed in) (?:amperes|amps|volts|meters|metres|seconds|milliseconds|microseconds|degrees|radians|hertz|Hz|percent)\b"
REPEATS_TYPE = r"\((?:integer |int )?(?:bitmask|enum|boolean|bool|int32|float)\)"
NUMBERED_OPTION = re.compile(r"(?:^|\s)-?\d{1,2}\s?(?::|-|–|\))\s", re.M)
PARAM_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]{1,}_[A-Z0-9_]*[A-Z0-9]\b")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def read_file(repo, ref, path):
    if ref == "WORKTREE":
        full = os.path.join(repo, path)
        if not os.path.exists(full):
            return None
        with open(full, encoding="utf-8") as f:
            return f.read()
    r = git(repo, "show", f"{ref}:{path}")
    return r.stdout if r.returncode == 0 else None


def scalar(node):
    return node.value if isinstance(node, yaml.ScalarNode) else None


def mapping_get(node, key):
    if not isinstance(node, yaml.MappingNode):
        return None, None
    for k, v in node.value:
        if scalar(k) == key:
            return k, v
    return None, None


def params_in(text):
    """Return {name: info} for every parameter definition in a module YAML text."""
    out = {}
    if text is None:
        return out
    try:
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        print(f"  YAML parse error: {e}")
        return out
    _, groups = mapping_get(root, "parameters")
    if not isinstance(groups, yaml.SequenceNode):
        return out
    for g in groups.value:
        _, defs = mapping_get(g, "definitions")
        if not isinstance(defs, yaml.MappingNode):
            continue
        for kname, pnode in defs.value:
            name = scalar(kname)
            info = {"line": kname.start_mark.line + 1, "short": "", "long": "",
                    "short_line": None, "long_line": None, "long_style": None,
                    "labels": {}, "labels_line": None, "type": None, "unit": None,
                    "meta": {}}
            _, desc = mapping_get(pnode, "description")
            ks, vs = mapping_get(desc, "short")
            if vs is not None:
                info["short"], info["short_line"] = vs.value, ks.start_mark.line + 1
            kl, vl = mapping_get(desc, "long")
            if vl is not None:
                info["long"], info["long_line"] = vl.value, kl.start_mark.line + 1
                info["long_style"] = vl.style  # '|', '>', "'", '"' or None (plain)
            for key in ("values", "bit"):
                kv, vv = mapping_get(pnode, key)
                if isinstance(vv, yaml.MappingNode):
                    info["labels"] = {scalar(a): scalar(b) for a, b in vv.value}
                    info["labels_line"] = kv.start_mark.line + 1
            if isinstance(pnode, yaml.MappingNode):
                for k, v in pnode.value:
                    key = scalar(k)
                    if key in ("description", "values", "bit"):
                        continue
                    info["meta"][key] = yaml.serialize(v).strip() if not isinstance(v, yaml.ScalarNode) else v.value
            info["type"] = info["meta"].get("type")
            info["unit"] = info["meta"].get("unit")
            out[name] = info
    return out


def desc_size(p):
    return len(p["short"]) + len(p["long"]) + sum(len(v or "") for v in p["labels"].values())


def known_param_names(repo, ref):
    """Approximate set of parameter names defined in the tree at ref, as regexes."""
    names = set()
    if ref == "WORKTREE":
        r = subprocess.run(["git", "-C", repo, "grep", "-h", "-E", r"^\s+[A-Z][A-Z0-9_${}]+:\s*$", "--", "*.yaml"],
                           capture_output=True, text=True)
        r2 = subprocess.run(["git", "-C", repo, "grep", "-h", "-o", "-E", r"PARAM_DEFINE_[A-Z0-9]+\([A-Z0-9_]+", "--", "*.c", "*.cpp", "*.h"],
                            capture_output=True, text=True)
    else:
        r = git(repo, "grep", "-h", "-E", r"^\s+[A-Z][A-Z0-9_${}]+:\s*$", ref, "--", "*.yaml")
        r2 = git(repo, "grep", "-h", "-o", "-E", r"PARAM_DEFINE_[A-Z0-9]+\([A-Z0-9_]+", ref, "--", "*.c", "*.cpp", "*.h")
    for line in r.stdout.splitlines():
        n = line.split(":")[-2].strip() if line.count(":") > 1 else line.strip().rstrip(":")
        names.add(n)
    for line in r2.stdout.splitlines():
        names.add(line.split("(")[-1])
    regexes = [re.compile("^" + re.escape(n).replace(r"\$\{i\}", r"\d+") + "$") for n in names if "${i}" in n]
    return {n for n in names if "${i}" not in n}, regexes


def param_exists(tok, known):
    plain, regexes = known
    return tok in plain or any(r.match(tok) for r in regexes)


def flags_for(name, p, old, known):
    f = []
    s, l, labels = p["short"], p["long"], p["labels"]
    if len(s) > SHORT_MAX:
        f.append((p["short_line"], f"short is {len(s)} chars (schema max {SHORT_MAX})"))
    if re.search(REPEATS_TYPE, s, re.I):
        f.append((p["short_line"], "short repeats the type"))
    if l:
        lnorm, snorm = l.strip().lower().rstrip("."), s.strip().lower().rstrip(".")
        if snorm and lnorm.startswith(snorm):
            f.append((p["long_line"], "long starts by restating short"))
        for pat in BOILERPLATE:
            m = re.search(pat, l, re.I)
            if m:
                f.append((p["long_line"], f"boilerplate: '{m.group(0)}'"))
        for pat in SYMBOL_WORDS:
            m = re.search(pat, l)
            if m:
                f.append((p["long_line"], f"symbol used as a word: '{m.group(0).strip()}'"))
        for pat, stock in STOCK_VARIANTS:
            m = re.search(pat, l, re.I)
            if m:
                f.append((p["long_line"], f"non-stock wording '{m.group(0)}': stock phrase is \"{stock}\""))
        if not p["unit"]:
            m = re.search(UNIT_WORDS, l, re.I)
            if m:
                f.append((p["long_line"], f"unit in prose ('{m.group(0)}') and no unit: field"))
        if labels:
            hits = NUMBERED_OPTION.findall(l)
            if len(hits) >= 2:
                f.append((p["long_line"], f"long appears to re-list numbered options ({len(hits)} matches)"))
            lab_texts = {str(v).strip().lower() for v in labels.values() if v}
            for line in l.splitlines():
                m = re.match(r"\s*([^:]{2,60}):\s", line)
                if m and len(l.splitlines()) > 1:
                    lab = m.group(1).strip().lower()
                    if lab not in lab_texts and lab not in ("warning", "note", "e.g"):
                        f.append((p["long_line"], f"per-option line label '{m.group(1).strip()}' matches no option label"))
        lines = l.split("\n")
        if p["long_style"] == "|" and len(lines) > 1:
            wrapped = False
            for a, b in zip(lines, lines[1:]):
                if a.strip() and b.strip() and not re.search(r"[.:!?]$", a.strip()) and b.strip()[:1].islower():
                    f.append((p["long_line"], f"literal block wrapped mid-sentence: '...{a.strip()[-25:]}' / '{b.strip()[:25]}...'"))
                    wrapped = True
                    break
            if not wrapped:
                for line in lines:
                    t = line.strip()
                    if re.match(r"[^:]{2,60}:\s", t) and not re.search(r"[.!?]$", t):
                        f.append((p["long_line"], f"per-option line without a full stop (lines are joined into one paragraph on the docs page): '{t[-40:]}'"))
                        break
    for tok in set(PARAM_TOKEN.findall(s + " " + l + " " + " ".join(str(v) for v in labels.values()))):
        if tok != name and not param_exists(tok, known) and not re.search(r"^(MAV_|MAV_CMD|MAVLINK|UAVCAN_V)", tok):
            f.append((p["long_line"] or p["short_line"], f"references '{tok}', not found among parameter definitions (confirm: may be a MAVLink/uORB name)"))
    if old is not None and old["labels"]:
        for k, v in old["labels"].items():
            if k not in labels:
                f.append((p["labels_line"], f"option {k} ('{v}') removed from labels"))
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", help="base ref (merge-base); omit with --all")
    ap.add_argument("--head", required=True, help="head ref, or WORKTREE for the working tree")
    ap.add_argument("--scratch", required=True, help="scratch dir outside the clone")
    ap.add_argument("--all", action="store_true", help="audit every parameter in the files as new")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()

    known = known_param_names(a.repo, a.head)
    tot_old = tot_new = 0
    for path in a.files:
        new_text = read_file(a.repo, a.head, path)
        old_text = None if a.all or not a.base else read_file(a.repo, a.base, path)
        new, old = params_in(new_text), params_in(old_text)
        print(f"=== {path}")
        for name in sorted(set(new) | set(old), key=lambda n: new.get(n, old.get(n, {"line": 0}))["line"]):
            n, o = new.get(name), old.get(name)
            if n is None:
                print(f"- {name}: removed")
                tot_old += desc_size(o)
                continue
            if o is None:
                cls = "new"
            elif (n["short"], n["long"], n["labels"]) != (o["short"], o["long"], o["labels"]):
                cls = "rewritten"
            elif n["meta"] != o["meta"]:
                cls = "metadata-only"
            else:
                continue  # untouched
            before = desc_size(o) if o else 0
            after = desc_size(n)
            tot_old += before
            tot_new += after
            changed = []
            if o:
                changed = [k for k in ("short", "long", "labels") if n[k] != o[k]]
                meta_changed = [k for k in set(n["meta"]) | set(o["meta"]) if n["meta"].get(k) != o["meta"].get(k)]
                changed += [f"meta:{k}" for k in meta_changed]
            print(f"- {name}: {cls} (line {n['line']}; short L{n['short_line']}, long L{n['long_line']}, "
                  f"labels L{n['labels_line']}; type {n['type']}; unit {n['unit']}; "
                  f"chars {before} -> {after}{'; changed ' + ', '.join(changed) if changed else ''})")
            for line, msg in flags_for(name, n, o, known):
                print(f"    L{line}: {msg}")
        if new_text is not None:
            dest = os.path.join(a.scratch, "validate", path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(new_text)

    if tot_old:
        print(f"\nDescription text (short + long + option labels) of changed parameters: "
              f"{tot_old} -> {tot_new} chars ({(tot_new - tot_old) * 100 / tot_old:+.1f}%)")
    else:
        print(f"\nDescription text of changed parameters: {tot_new} chars")

    # Schema validation, using the head's own validator and schema, on scratch copies.
    vdir = os.path.join(a.scratch, "validate")
    for tool in ("Tools/validate_yaml.py", "validation/module_schema.yaml"):
        text = read_file(a.repo, a.head, tool)
        if text is None:
            print(f"\nValidator not run: {tool} not found at {a.head}")
            return
        dest = os.path.join(vdir, "_tool", os.path.basename(tool))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
    targets = [os.path.join(vdir, p) for p in a.files if os.path.exists(os.path.join(vdir, p))]
    r = subprocess.run([sys.executable, os.path.join(vdir, "_tool", "validate_yaml.py"),
                        "--schema-file", os.path.join(vdir, "_tool", "module_schema.yaml"), *targets],
                       capture_output=True, text=True)
    out = (r.stdout + r.stderr).replace(vdir + "/", "")
    print(f"\nTools/validate_yaml.py exit {r.returncode}" + (f":\n{out}" if out.strip() else ": no errors"))


if __name__ == "__main__":
    main()
