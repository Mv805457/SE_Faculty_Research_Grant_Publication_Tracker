# Lab 4 · Tic-Tac-Toe · Course starter 09

The player is X. Click an empty square, and the computer plays O. Press X or O to select who opens the next round. R starts a round and retains the scoreboard. M resets the match totals.

```sh
python -m pip install -r requirements.txt
python main.py
python -m unittest -v
```

The revised rules enumerate eight winning lines. The move handler checks for a winner before declaring a full-board draw, rejects occupied cells, and freezes the board after a terminal move. Each terminal transition awards exactly one scoreboard point.

**Recording evidence.** Watch [the original starter](before.mp4) and [the corrected game](after.mp4). They replay the same opening clicks and random seed through the game engine. In the second recording the X diagonal ends the round and the next round retains its point. The starter repository and its exercise instructions are available [on GitHub](https://github.com/SETAPESU26/09_tic_tac_toe/tree/28263985b9846c3f5a716dd971f91ee752223a04).

The handout also requests a shared conversation link. Create that link from this chat for your individual submission.
