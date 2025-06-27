# NEW_CARD_COUNTING

This project demonstrates a simple Hi-Lo card counting tool written with
PyQt5.  The application keeps track of the running and true counts while you
enter cards that have been played.

## Usage
1. Install the dependencies (`PyQt5`).
2. Run the GUI:
   ```bash
   python New_card_count.py
   ```
3. Choose the number of decks in play.
4. Type card values separated by spaces (e.g. `10 K 3`).
5. Press **Calculate** to update the count or **Reset** to start over.

The program displays betting advice based on the true count and shows images of
red or black cards depending on the suggestion.
