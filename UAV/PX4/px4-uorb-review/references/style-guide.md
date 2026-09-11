# uORB message documentation standard

Extracted from <https://docs.px4.io/main/en/uorb/uorb_documentation>, cross-checked against `Tools/msg/generate_msg_docs.py` (the project's own parser/validator, which is ground truth where the two differ — the script is versioned with the code it documents, the page can lag).

## Comment syntax

`#` starts a comment; everything after it on the line is comment text.
A line beginning `# TOPICS` is reserved (see Multi-topic messages below) and is never prose.
A comment line that appears after a field/constant's own documentation, with no field or constant attached to it, is an "internal comment" — it's for maintainers reading the `.msg` source and never appears in the generated docs.

## Message-level description

The comment block at the very top of the file, before the first field or constant:

1. **Short description — mandatory.** One line, concise, no terminal period. E.g. `# Validated airspeed`.
2. **Blank comment line — optional.** Separates short from long description.
3. **Long description — optional.** Further context: usage, publishers/consumers, frame restrictions, operational modes. Normal punctuation, may span multiple lines.

The block ends at the first blank line or the first field/constant.
A message with no short description at all is flagged by the tool as `summary_missing`.

## Field-level documentation

Comment goes on the same line as the declaration:

```
type field_name # [metadata] Description
```

Metadata is one or more bracketed tags, in any order, all optional except units:

| Tag | Form | Notes |
| --- | --- | --- |
| Units | `[<unit>]` | No `@` prefix. Required unless the field is `bool` or purely enum-valued. Unitless numeric fields use `[-]`. |
| Enum reference | `[@enum <PREFIX>]` | Marks this field as selected by constants whose names start `<PREFIX>_`. |
| Valid range | `[@range <lower>, <upper>]` | Either bound may be blank for unbounded, e.g. `[@range 5.3, ]`. |
| Invalid-value sentinel | `[@invalid <value> <description>]` | Description optional. `<value>` must be one of `NaN`, `0`, `-1`, `UINT8_MAX`, `UINT16_MAX`. |
| Reference frame | `[@frame <value>]` | One of `NED`, `Body`, `FRD`, `ENU`. |

Allowed units (from the parser's own list — treat as authoritative):
`m`, `m/s`, `m/s^2`, `(m/s)^2`, `deg`, `deg/s`, `rad`, `rad/s`, `rad^2`, `rpm`, `V`, `A`, `mA`, `mAh`, `W`, `Wh`, `dB`, `dBm`, `h`, `minutes`, `s`, `ms`, `us`, `Hz`, `MHz`, `Ohm`, `MB`, `KiB/s`, `Kb/s`, `degC`, `Pa`, `%`, `norm`, `-`.

Description text: starts with a capital letter, omits the terminal period for a single-sentence description; a multi-sentence description punctuates normally throughout (including its final sentence).

## Constants

```
type NAME = value # Description
```

No metadata tags on constants — description only.

**Enum grouping.** Constants sharing a prefix are declared immediately beneath the field they apply to, and that field carries the matching `[@enum PREFIX]` tag:

```
int8 airspeed_source # [@enum SOURCE] Source description
int8 SOURCE_DISABLED = -1 # Disabled
int8 SOURCE_GROUND_MINUS_WIND = 0 # Ground speed minus wind
```

A constant whose prefix doesn't match any field's `@enum` tag is flagged by the tool as `constant_not_in_assigned_enum`.

**Exempt from documentation.** `ORB_QUEUE_LENGTH` and `MESSAGE_VERSION` need no comment — the tool never asks for one.

## Multi-topic messages

```
# TOPICS topic_name_1 topic_name_2
# TOPICS topic_name_3
```

Declares that one message struct backs several uORB topics. No standardised format exists yet for documenting *why* — don't invent a requirement here that the standard doesn't state.

## General

- A comment line placed after all fields/constants, or between two fields with no declaration of its own, is an "internal comment": intended for maintainers, not readers of the generated docs, and not checked for prose quality.
- Field/constant descriptions shouldn't just restate the name (`uint8 mode # Mode` says nothing a reader doesn't already have).
- Whitespace: a single space between the declaration and `#`; the tool flags trailing whitespace, leading whitespace before a field/constant, and multiple consecutive spaces inside a field/constant name as notes.
