# Accessibility Notes — tan(x) Calculator GUI

## Color contrast (WCAG 2.1 AA — 4.5:1 for normal text)

Computed using the standard WCAG relative-luminance / contrast-ratio
formula against each widget's actual foreground/background pair:

| Text | Background | Ratio | WCAG AA (4.5:1) |
|------|-----------|-------|------------------|
| Black result/label text | white | 21.00:1 | Pass |
| Error text `#c0392b` | white | 5.44:1 | Pass |
| Hint text `#666666` | white | 5.74:1 | Pass |
| White button text | `#4a7abc` (original) | 4.37:1 | **Fail** |
| White button text | `#3a6aac` (updated) | 5.47:1 | Pass |

The button background was the only failure, and only by a small
margin (button text is 11pt bold, which doesn't qualify as WCAG
"large text," so it needs the full 4.5:1, not the relaxed 3:1). It
was darkened from `#4a7abc` to `#3a6aac` to clear the threshold
without materially changing the color identity of the UI.

## Explicit light theme (bg pinning)

Before this pass, no widget set an explicit background color, so
each one inherited whatever the OS theme provided. Under macOS Dark
Mode specifically, Tkinter's classic (non-ttk) widgets don't
automatically pair a dark background with light text — the result is
hardcoded dark text (e.g. `fg="black"`) landing on a dark background,
which is unreadable. Every widget now sets `bg=self.BG` (`"white"`)
explicitly, so contrast is guaranteed regardless of the user's system
theme, rather than being an accident of whatever theme happens to be
active.

## Keyboard navigation

- Tab order follows widget creation order: entry field → radio
  buttons → compute button, which matches the natural top-to-bottom
  reading order of the form.
- The entry field receives focus automatically on launch
  (`self.entry_x.focus()`), so a keyboard-only user can start typing
  immediately without tabbing to find the input.
- Enter/Return in the entry field triggers the same action as
  clicking "Compute tan(x)" (`self.entry_x.bind("<Return>", ...)`),
  so the primary action never requires a mouse.
- Radiobuttons and the Button widget are natively focusable and
  activatable via Tab + Space/Return — this is Tkinter's default
  behavior for these widget classes and required no extra code.

## Labels

Every input has a visible, persistent text label (`"Enter x:"`,
`"Unit:"`) rather than placeholder-only text that disappears on
focus, so the purpose of each control remains visible throughout
interaction — this also happens to be what most screen readers rely
on when Tkinter widgets don't expose richer accessibility metadata
(Tkinter's own screen-reader/AT support is limited compared to native
toolkits, so a visible, unambiguous label is the most reliable thing
this stack can guarantee).

## Font sizes

Primary label/entry/result text is 11pt, the compute button is 11pt
bold, and only the supplementary input-format hint is smaller (9pt,
compensated by its higher 5.74:1 contrast ratio). No interactive
element relies on text smaller than 9pt.
