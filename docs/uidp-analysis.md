# UI Design Principles (UIDP) Analysis — tan(x) Calculator GUI

Two established UIDP sets were considered: **Nielsen's 10 Usability
Heuristics** and **Shneiderman's Eight Golden Rules**. They overlap
heavily (both target general interactive-system usability), so
Nielsen's 10 are used as the primary checklist below, with
Shneiderman's rules folded in where they add something Nielsen's set
doesn't cover explicitly. This file records the applies /
doesn't-apply reasoning per principle; the mind map diagram grouping
these into "applies" vs. "doesn't apply" clusters is built separately.

Target system: a **single-user, single-screen, stateless Tkinter
desktop calculator** — one input, one unit choice, one action
(compute), one result. That shape rules a few principles out by
construction and makes others especially load-bearing.

## Nielsen's 10 Heuristics

| # | Heuristic | Applies? | Reasoning |
|---|-----------|----------|-----------|
| 1 | Visibility of system status | **Yes** | The result label must update immediately after "Compute" is pressed, and must visibly distinguish a normal result from an error (color change), so the user always knows what state the last computation is in. |
| 2 | Match between system and the real world | **Yes** | Labels use plain terms a calculator user already knows ("Enter x:", "Radians"/"Degrees"), and error text is written in everyday language ("not a valid number") instead of exposing Python exception class names. |
| 3 | User control and freedom | **Partially** | There's no destructive action to undo (a calculation can't corrupt data), so "undo/redo" is moot. What does apply: the user can freely edit the entry field and recompute at will, with no lock-in to a previous input. |
| 4 | Consistency and standards | **Yes** | One font family/size scheme, one button style, and the OS-standard convention that Enter submits a single-field form. |
| 5 | Error prevention | **Yes** | Before this pass, the only prevention was reactive (catch and report). Added a hint under the input showing an example value, so malformed input is less likely in the first place, not just handled after the fact. |
| 6 | Recognition rather than recall | **Yes** | Unit is chosen via visible radio buttons, not a remembered code or flag; the user never has to recall a syntax. |
| 7 | Flexibility and efficiency of use | **Yes** | Enter-to-submit is a shortcut for repeat use; the same action is also reachable by mouse click, so it doesn't cost novice users anything. |
| 8 | Aesthetic and minimalist design | **Yes** | Exactly four widgets carry the whole interaction (entry, unit choice, button, result). Nothing decorative competes with the task. |
| 9 | Help users recognize, diagnose, and recover from errors | **Yes** | This is the heaviest-weighted heuristic here, since it's also required functionally by Problem 5. Both failure modes (non-numeric input, mathematically undefined tan(x)) produce a specific, plain-language message rather than a stack trace or silent failure. |
| 10 | Help and documentation | **No** | The task surface is small enough (one field, one choice, one button) that in-app help would be overhead, not assistance. External documentation (the README) covers setup/usage instead; this heuristic doesn't drive any in-GUI change. |

## Shneiderman's Eight Golden Rules — anything not already covered above

| Rule | Applies? | Reasoning |
|------|----------|-----------|
| Support internal locus of control | **Yes** | Nothing happens unless the user presses Compute (or Enter); there's no auto-recompute or background behavior that could feel like the system is "acting on its own." |
| Reduce short-term memory load | **Yes** | Everything needed for the current task is visible on one screen at once; there's no multi-step wizard requiring the user to remember earlier input. |
| Design for closure | **Partially** | Each compute action reaches a clear end-state (a result or an error is shown), but since the tool is meant for repeated one-off calculations rather than a multi-step "task" with a final completion, this rule applies more weakly than in a form-submission-style app. |

## Explicitly does not apply

Principles or sub-clauses oriented at **multi-user awareness**,
**permissions/roles**, **collaborative editing conflict resolution**,
or **deep navigational hierarchies** (common in heuristic checklists
aimed at web apps or collaborative tools) do not apply here at all —
this is a single-user, single-window, non-networked desktop tool with
no navigation beyond the one screen it opens on.

## Changes made to `tan_gui.py` as a result of this analysis

1. **Error prevention / recognition (heuristics 5, 6):** added a
   small gray hint label under the input field showing an example
   value format, so the expected input shape is visible before the
   user ever gets it wrong.
2. **Visibility of system status (heuristic 1):** the result label
   now resets to a neutral "awaiting input" state as soon as the
   user starts editing the entry field again, instead of leaving a
   stale red error message on screen that no longer corresponds to
   the (as yet unsubmitted) current input.

No changes were made to `tan_core.py` — this analysis is purely about
the GUI layer.
