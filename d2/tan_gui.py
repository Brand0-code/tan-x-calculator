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

Theming note: this GUI forces the ttk "clam" theme instead of the
platform-native theme. On macOS, the native "aqua" theme silently
ignores explicit bg/fg colors on most widgets and instead follows the
OS light/dark mode - so a hardcoded light theme could still render as
unreadable text on a dark system background. "clam" is a pure-Tcl
theme that actually honors the colors set below on every platform.
"""

import tkinter as tk
from tkinter import ttk

from tan_core import tan_taylor, degrees_to_radians, UndefinedTangentError

BG = "#ffffff"
FG = "#000000"
HINT_FG = "#666666"
ERROR_FG = "#c0392b"
BUTTON_BG = "#3a6aac"
BUTTON_ACTIVE_BG = "#2f5a94"
BUTTON_FG = "#ffffff"


class TanCalculatorGUI:
    # pylint: disable=too-few-public-methods
    # A Tkinter widget-wrapper class naturally exposes one public
    # entry point (the compute handler); the rest of its behavior is
    # wired up as widget callbacks in __init__, not separate public
    # methods. Splitting it further would add indirection with no
    # benefit here.
    """Tkinter GUI for computing tan(x) via the from-scratch tan_core module."""

    def __init__(self, root):
        self.root = root
        root.title("tan(x) Calculator - SOEN 6011 F2")
        root.geometry("440x310")
        root.resizable(False, False)
        root.configure(bg=BG)

        self._init_style()

        # --- Input row ---
        ttk.Label(root, text="Enter x:").grid(
            row=0, column=0, padx=12, pady=(15, 5), sticky="w")
        self.entry_x = ttk.Entry(root, width=20)
        self.entry_x.grid(row=0, column=1, padx=12, pady=(15, 5))
        self.entry_x.focus()

        # --- Input hint (error prevention / recognition-over-recall) ---
        # #666666 on white = 5.74:1 contrast, clears WCAG AA (4.5:1).
        ttk.Label(root, text="e.g. 0.5, 45, or -1.2", style="Hint.TLabel").grid(
            row=1, column=1, padx=12, sticky="w")

        # --- Unit selection ---
        ttk.Label(root, text="Unit:").grid(row=2, column=0, padx=12, sticky="w")
        self.unit_var = tk.StringVar(value="radians")
        unit_frame = ttk.Frame(root)
        unit_frame.grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(unit_frame, text="Radians", variable=self.unit_var,
                        value="radians").pack(side="left")
        ttk.Radiobutton(unit_frame, text="Degrees", variable=self.unit_var,
                        value="degrees").pack(side="left")

        # --- Compute button ---
        # BUTTON_BG "#3a6aac" gives a 5.47:1 contrast ratio against the
        # white button text, clearing WCAG AA (4.5:1) for normal-size
        # text (the original #4a7abc measured 4.37:1, just short).
        self.compute_btn = ttk.Button(
            root, text="Compute tan(x)", command=self.on_compute,
            style="Compute.TButton")
        self.compute_btn.grid(row=3, column=0, columnspan=2, pady=18)

        # --- Result / error display ---
        # black-on-white = 21:1, error red #c0392b-on-white = 5.44:1;
        # both comfortably clear WCAG AA (4.5:1) for normal-size text.
        self.result_var = tk.StringVar(value="Result will appear here.")
        self.result_label = ttk.Label(
            root, textvariable=self.result_var, wraplength=400,
            style="Result.TLabel", justify="left", anchor="w")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=12,
                               pady=5, sticky="w")

        # Allow pressing Enter in the entry field to trigger compute
        self.entry_x.bind("<Return>", lambda event: self.on_compute())

        # Visibility of system status: a stale error/result shouldn't
        # look like it still describes the input once the user starts
        # editing it again.
        self.entry_x.bind("<Key>", self._on_entry_edited)

    @staticmethod
    def _init_style():
        """Force the 'clam' ttk theme so custom colors render on every OS."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG,
                        font=("Arial", 11))
        style.configure("Hint.TLabel", background=BG, foreground=HINT_FG,
                        font=("Arial", 9))
        style.configure("Result.TLabel", background=BG, foreground=FG,
                        font=("Arial", 11))
        style.configure("Error.TLabel", background=BG, foreground=ERROR_FG,
                        font=("Arial", 11))
        style.configure("TRadiobutton", background=BG, foreground=FG,
                        font=("Arial", 10))
        style.map("TRadiobutton", background=[("active", BG)])
        style.configure("TEntry", fieldbackground=BG, foreground=FG)
        style.configure("Compute.TButton", background=BUTTON_BG,
                        foreground=BUTTON_FG, font=("Arial", 11, "bold"),
                        padding=(10, 5))
        style.map(
            "Compute.TButton",
            background=[("active", BUTTON_ACTIVE_BG)],
            foreground=[("active", BUTTON_FG)],
        )

    def _on_entry_edited(self, _event):
        """Reset the result display to neutral once the input is edited again."""
        self.result_var.set("Result will appear here.")
        self.result_label.config(style="Result.TLabel")

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
            self.result_label.config(style="Error.TLabel")
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
            self.result_label.config(style="Result.TLabel")
        except UndefinedTangentError as e:
            self.result_var.set(f"Error: {e}")
            self.result_label.config(style="Error.TLabel")


def main():
    """Launch the tan(x) calculator GUI."""
    root = tk.Tk()
    TanCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
