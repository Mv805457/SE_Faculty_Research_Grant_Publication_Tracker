# Seat reservation findings

Line numbers refer to the original course starter.

| Issue | Type and location | Observed consequence | Correction |
|---|---|---|---|
| Overly permissive file mode | High, permissions, line 55 | The program requests read, write and execute access for everyone on POSIX. | Write through a private temporary file and replace the destination after serialization. |
| Invalid seat numbers | High, business rule, lines 9–16, 45–47 | The supplied demonstration accepts 25 for a 20-seat show, −1 and the string A7. | Accept whole seat numbers from 1 to capacity and reject duplicate bookings. |
| Duplicate logical bookings | High, input type, lines 50–51 | The CLI passes a string. It can reserve the same seat as an existing integer booking. | Parse the user’s input once and validate it in the reservation function. |
| Swallowed errors | Medium, handling, lines 18–22 | A missing show or seat silently disappears in a bare exception handler. | Check membership and return an explicit release result. |
| Partial writes and open handles | Medium, persistence, lines 27–35 | The destination is truncated before serialization completes. Files lack deterministic closure. | Use context managers, atomic replacement and validation before replacing memory state. |
| MD5 and ambiguous identifiers | Medium, reference generation, lines 24–25 | Concatenating A1 + 2 and A + 12 produces the same input. Bandit flags MD5. | Hash a structured show/seat pair with SHA-256. The eight-character code is a display reference. |
| Shared default list | Low, state lifetime, line 9 | Calls without a log argument share an inaccessible log list. | Allocate no implicit log and append only when the caller supplies one. |
