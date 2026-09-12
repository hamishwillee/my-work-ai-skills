# Lens: accuracy

Every factual claim on an in-scope page is one of two kinds, and each kind has its own bar:

## Protocol-level claims (checked against the XML)

Anything about a param's existence, number, name, description, units, values, or default — the things the MAVLink XML itself defines — is checked against the matching entry in `en/messages/<dialect>.md` (see `references/shared.md` for how to reach it).

- The param exists at the number/name claimed.
- The description doesn't contradict what the XML says it does.
- A stated range, unit, or enum value matches.
- A claim that a field "applies to" or "is defined for" a given command is a protocol-level claim if it's about whether the field exists/is documented for that command in the XML — this is confirmable by reading the XML entry, independent of whether any autopilot actually honors it (that's an implementation-level claim, below).

A mismatch here is `bug`, handled per `references/shared.md`, "When the doc and the XML disagree" — never resolved by just picking a side.

## Implementation-level claims (need a citable source)

Anything about what a *specific autopilot* actually does — "ArduPilot does X," "not supported on PX4," "multicopters circle for this command," "has no practical effect for Y" — is not answerable from the XML, because the XML defines the protocol, not any one implementation's behaviour.

- A claim like this needs a citation: a file/line in the ArduPilot or PX4 source, a linked test, or a linked GitHub issue/PR discussion where the behaviour was actually established.
- No citation attached → `style`, not `bug`, and not silently accepted either: name it as an unevidenced claim in the report. See `references/shared.md`, Severity, for why the tier split matters here.
- A citation that turns out to contradict what it's cited for is a `bug` — worse than no citation, since it reads as verified when it isn't.
- "This seems like reasonable behaviour" or "this is probably how it works" is never sufficient, including when an LLM produced the reasoning — flag it exactly the same as an unsupported claim from a person.
- A claim phrased as speculation ("likely has no practical effect," "probably synonymous with") is still `style` if uncited, but is a smaller ask to close out: a reviewer just needs one citation to promote it, versus a bare assertion which needs either a citation or removal.

## What doesn't need a citation

- A restatement of something the XML already documents, in different words, as long as the meaning is unchanged — that's still a protocol-level claim, checked as above, not an uncited implementation claim.
- A cross-reference to another section on the same page ("see Exit Conditions above") is structural, not a factual claim, and needs no citation of its own — though whether the params it points at actually share that behaviour is still a protocol-level or implementation-level claim in its own right, checked the normal way.
- General, non-specific framing ("a fixed-wing vehicle circles the point") doesn't need a citation if it matches what the XML's own command description already says in prose; it does need one the moment it gets more specific than that ("ArduPilot's implementation of this circles even for multicopters, unlike every other loiter command").

## Newly invented sections

A page that adds a subsection with no established precedent on that page (most commonly "Autopilot Support") needs the same evidence bar as any other implementation-level claim, for every bullet in it — a whole new section is not exempt just because sibling commands elsewhere on the page happen to have one already.
A subsection with no evidenced content to put in it should not be invented speculatively; an explicitly placeholder version (a single "untested"/"unverified" bullet, commented out of rendered output if the author wants it there as a reminder without publishing it) is fine and is not itself a finding.
