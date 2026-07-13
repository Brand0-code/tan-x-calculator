# Changelog

This project uses [Semantic Versioning](https://semver.org/)
(MAJOR.MINOR.PATCH).

## [v1.0.0] — D3 polish pass (first stable release)

- Fixed all Flake8-flagged PEP-8 violations in `tan_core.py` and
  `tan_gui.py` (5 -> 0).
- Addressed all reasonable Pylint warnings; score 9.43/10 -> 10.00/10.
- Added a UIDP analysis (`docs/uidp-analysis.md`) and applied the
  applicable principles to the GUI: an input-format hint and a
  status reset on re-edit.
- Accessibility pass: fixed a button-text contrast ratio that fell
  short of WCAG AA (4.37:1 -> 5.47:1), and pinned an explicit light
  theme so contrast doesn't depend on OS dark/light mode.
- Added a `unittest` (PyUnit) suite covering known values, undefined
  points, precision vs. `math.tan()`, and the from-scratch
  subordinate helper functions — 14/14 passing.
- Captured Flake8, pdb, and Pylint tool-usage evidence under `docs/`.

## [v0.2.0] — D2: from-scratch implementation + GUI

- Implemented `tan_core.py`: tan(x) via Taylor series, built from
  scratch (no built-in/library functions beyond arithmetic, I/O, and
  UI), including from-scratch `my_abs()`, `my_factorial()`, and
  `degrees_to_radians()`.
- Implemented `tan_gui.py`: a Tkinter GUI wrapping `tan_core.py`,
  with exception handling for invalid and mathematically undefined
  input.
- Published the source to a public GitHub repository with a README
  and descriptive commit history.

## [v0.1.0] — D1: CLI implementation

- Implemented `tan_calculator.py`: a textual (CLI) tan(x) calculator
  using Python's `math` module and a Taylor series expansion of
  sin(x)/cos(x).
