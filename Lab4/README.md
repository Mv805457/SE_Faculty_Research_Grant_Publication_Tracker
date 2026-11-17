# Lab 4 · Grant Desk

The [course problem 09 Tic-Tac-Toe solution](09_tic_tac_toe/) includes the corrected starter, regression tests and two gameplay recordings. The faculty-themed exercise below follows the mechanics of the comparison repository.

A research-office arcade exercise adapted to the faculty tracker topic. Move the intake tray to file falling grant applications and manuscripts. Five missed documents close the shift.

```sh
python -m pip install -r requirements.txt
python main.py
python main.py --baseline
python -m unittest -v
```

Use the arrow keys to move, Space for a 1.6-second speed boost, and R to restart. A four-second cooldown starts at activation.

| Change | How to verify it |
|---|---|
| Require vertical and horizontal overlap | In the [baseline recording](before.mp4), the opening grant and paper disappear at the top. In the [revised recording](after.mp4), they reach the intake tray before the counts change. |
| Process each arrival once | Two cards reach the tray together in the revised recording. Both counters advance on the same update. |
| Keep the tray on screen | Hold either arrow until the tray stops. Its outer edge stays inside the window. |
| Pace incoming work | The scheduler varies spawn intervals, chooses a different lane each time and caps the number of active cards at five. |
| Provide temporary faster movement | Space changes the tray color and speed. The footer displays the boost and cooldown states. |

Both ten-second recordings use the same seed, inputs and rendering code as the interactive game. The scripted opening aligns two adjacent cards so the original defects are visible. The [development notes](development.md) explain the debugging decisions.
