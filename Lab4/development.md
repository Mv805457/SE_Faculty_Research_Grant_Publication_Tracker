# Debugging notes

The comparison starts in `baseline.py`. Its first rule considers a file received as soon as its horizontal range overlaps the tray. Its second rule shortens the list while traversing it, which can skip the card that shifts into the current slot.

The corrected `Desk.catches` checks both coordinate ranges. `file_cards` builds the list of cards still falling after counting each arrival or miss exactly once. The two regression tests isolate the failure modes: one aligned card high above the tray, and two cards arriving at the tray on the same frame.

Movement uses elapsed seconds and clamps the tray's left edge to the window width minus the tray width. A separate countdown controls the boost so holding the activation key cannot extend it indefinitely. The spawn timer and card cap keep gameplay predictable enough for the before/after comparison.

This is a summary of the implementation and tests from this session. A course submission that asks for a conversation URL can use the share link created by the student from this chat.
