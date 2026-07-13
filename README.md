# tan(x) Calculator — SOEN 6011

Scientific calculator function implementation for SOEN 6011: Software
Engineering Processes (Summer 2026, Concordia University).

**Assigned function:** F2 — tan(x)

## Structure

```
tan-x-calculator/
├── README.md
├── d1/
│   └── tan_calculator.py   # D1 CLI implementation (uses the math module)
├── d2/
│   ├── tan_core.py         # D2 from-scratch computation (no built-ins beyond arithmetic)
│   └── tan_gui.py          # D2 Tkinter GUI, imports from tan_core.py
└── docs/
    ├── gui_normal.png      # screenshot: normal (defined) result
    └── gui_error.png       # screenshot: undefined-input error handling
```

## Running

Requires Python 3.x. The D2 GUI additionally requires `tkinter`, which
ships with most Python installs; on Linux you may need to install it
separately (`sudo apt install python3-tk`).

**D1 — CLI version** (uses Python's `math` module):

```bash
python3 d1/tan_calculator.py
```

**D2 — GUI version** (from-scratch computation, no IDE required):

```bash
python3 d2/tan_gui.py
```

## Algorithm

tan(x) = sin(x) / cos(x), where sin(x) and cos(x) are each computed via
their Maclaurin (Taylor) series expansions, after reducing x into the
range [-pi, pi] for faster convergence. If cos(x) is within a small
epsilon of zero (x near an odd multiple of pi/2), tan(x) is undefined
and a descriptive error is raised.

## From-scratch implementation (D2)

`d2/tan_core.py` implements tan(x) without relying on any built-in or
library math functions — only arithmetic operators, input, output, and
UI-related functions are used, per the Deliverable 2 constraint. This
required writing subordinate helper functions from scratch:

| D1 (math module) | D2 (from scratch)   |
|-------------------|----------------------|
| `math.pi`         | `PI` (hardcoded constant) |
| `math.factorial`  | `my_factorial()`     |
| `math.radians`    | `degrees_to_radians()` |
| `abs()`           | `my_abs()`            |

`d2/tan_gui.py` wraps `tan_core.py` in a Tkinter GUI and handles both
invalid (non-numeric) input and mathematically undefined input
(`UndefinedTangentError`) with helpful, user-facing error messages.

## Requirements

Functional/non-functional requirements (ISO/IEC/IEEE 29148 style) are
tracked as part of the course deliverables and are not duplicated here.
