"""
tan(x) Tkinter GUI - built on top of the from-scratch core.

SOEN 6011 - Deliverable 2 - Problem 5
Function assigned: F2 = tan(x)

Run with: python3 tan_gui.py
No IDE required to compile or run.

"From scratch" boundary note: str.strip() (used on the raw entry-box
text before parsing) is treated as input handling, same category as
float() in tan_core.py's documented assumptions - not a computation
on the mathematical value itself.
"""

import tkinter as tk
from tan_core import tan_taylor, degrees_to_radians, UndefinedTangentError


class TanCalculatorGUI:
    # pylint: disable=too-few-public-methods
    # A Tkinter widget-wrapper class naturally exposes one public
    # entry point (the compute handler); the rest of its behavior is
    # wired up as widget callbacks in __init__, not separate public
    # methods. Splitting it further would add indirection with no
    # benefit here.
    """Tkinter GUI for computing tan(x) via the from-scratch tan_core module."""

    # Explicit light theme: Tkinter's classic widgets don't auto-adapt
    # fg/bg together under OS dark mode, which can otherwise silently
    # turn e.g. black-on-default-dark into unreadable text. Pinning
    # colors keeps contrast ratios (see comments below) predictable
    # regardless of the user's system theme.
    BG = "white"

    def __init__(self, root):
        self.root = root
        root.title("tan(x) Calculator - SOEN 6011 F2")
        root.geometry("440x310")
        root.resizable(False, False)
        root.config(bg=self.BG)

        # --- Input row ---
        tk.Label(root, text="Enter x:", font=("Arial", 11), bg=self.BG).grid(
            row=0, column=0, padx=12, pady=(15, 5), sticky="w")
        self.entry_x = tk.Entry(root, font=("Arial", 11), width=20,
                                bg=self.BG, fg="black")
        self.entry_x.grid(row=0, column=1, padx=12, pady=(15, 5))
        self.entry_x.focus()

        # --- Input hint (error prevention / recognition-over-recall) ---
        # #666666 on white = 5.74:1 contrast, clears WCAG AA (4.5:1).
        tk.Label(root, text="e.g. 0.5, 45, or -1.2", font=("Arial", 9),
                 fg="#666666", bg=self.BG).grid(
            row=1, column=1, padx=12, sticky="w")

        # --- Unit selection ---
        tk.Label(root, text="Unit:", font=("Arial", 11), bg=self.BG).grid(
            row=2, column=0, padx=12, sticky="w")
        self.unit_var = tk.StringVar(value="radians")
        unit_frame = tk.Frame(root, bg=self.BG)
        unit_frame.grid(row=2, column=1, sticky="w")
        tk.Radiobutton(unit_frame, text="Radians", variable=self.unit_var,
                       value="radians", font=("Arial", 10),
                       bg=self.BG).pack(side="left")
        tk.Radiobutton(unit_frame, text="Degrees", variable=self.unit_var,
                       value="degrees", font=("Arial", 10),
                       bg=self.BG).pack(side="left")

        # --- Compute button ---
        # bg="#3a6aac" gives a 5.47:1 contrast ratio against the white
        # button text, clearing the WCAG AA 4.5:1 threshold for normal-
        # size text (the original #4a7abc measured 4.37:1, just short).
        self.compute_btn = tk.Button(
            root, text="Compute tan(x)", command=self.on_compute,
            font=("Arial", 11, "bold"), bg="#3a6aac", fg="white",
            activebackground="#2f5a94", padx=10, pady=5)
        self.compute_btn.grid(row=3, column=0, columnspan=2, pady=18)

        # --- Result / error display ---
        # black-on-white = 21:1, error red #c0392b-on-white = 5.44:1;
        # both comfortably clear WCAG AA (4.5:1) for normal-size text.
        self.result_var = tk.StringVar(value="Result will appear here.")
        self.result_label = tk.Label(
            root, textvariable=self.result_var, font=("Arial", 11),
            wraplength=400, fg="black", bg=self.BG, justify="left", anchor="w")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=12,
                               pady=5, sticky="w")

        # Allow pressing Enter in the entry field to trigger compute
        self.entry_x.bind("<Return>", lambda event: self.on_compute())

        # Visibility of system status: a stale error/result shouldn't
        # look like it still describes the input once the user starts
        # editing it again.
        self.entry_x.bind("<Key>", self._on_entry_edited)

    def _on_entry_edited(self, _event):
        """Reset the result display to neutral once the input is edited again."""
        self.result_var.set("Result will appear here.")
        self.result_label.config(fg="black")

    def on_compute(self):
        """Read the entry field, compute tan(x), and update the result label."""
        raw_input = self.entry_x.get().strip()

        # --- Exception handling: invalid (non-numeric) input ---
        try:
            x_value = float(raw_input)
        except ValueError:
            self.result_var.set(
                f"Error: '{raw_input}' is not a valid number. "
                f"Please enter a numeric value, e.g. 0.5, 45, or -1.2."
            )
            self.result_label.config(fg="#c0392b")
            return

        # Unit conversion (REQ-005 / REQ-006 equivalent from D1)
        if self.unit_var.get() == "degrees":
            x_radians = degrees_to_radians(x_value)
        else:
            x_radians = x_value

        # --- Exception handling: undefined tan(x) ---
        try:
            result = tan_taylor(x_radians)
            unit_label = "deg" if self.unit_var.get() == "degrees" else "rad"
            self.result_var.set(f"tan({x_value} {unit_label}) = {result:.6f}")
            self.result_label.config(fg="black")
        except UndefinedTangentError as e:
            self.result_var.set(f"Error: {e}")
            self.result_label.config(fg="#c0392b")


def main():
    """Launch the tan(x) calculator GUI."""
    root = tk.Tk()
    TanCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
