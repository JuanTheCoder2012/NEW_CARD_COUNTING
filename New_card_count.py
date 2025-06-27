import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtGui import QPixmap

class CardCountingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Card Counting')
        self.running_count = 0
        self.decks = 8
        self.cards_per_deck = 52
        self.total_cards = self.decks * self.cards_per_deck

        self.cards_played = 0

        self.dealer_label = QLabel('Dealer cards (comma separated):')
        self.dealer_entry = QLineEdit(self)
        self.player_label = QLabel('Player cards (comma separated):')
        self.player_entry = QLineEdit(self)
        self.result_label = QLabel(self)
        self.advice_label = QLabel(self)
        self.red_card_image = QLabel(self)
        self.black_card_image = QLabel(self)

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate_count)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.exit_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.dealer_label)
        layout.addWidget(self.dealer_entry)
        layout.addWidget(self.player_label)
        layout.addWidget(self.player_entry)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.advice_label)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.red_card_image)
        images_layout.addWidget(self.black_card_image)
        layout.addLayout(images_layout)

        self.show()

    def parse_cards(self, text: str):
        text = text.replace(',', ' ')
        return [t.lower() for t in text.split() if t]

    def get_card_value(self, card: str):
        mapping = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'j': 11,
            'q': 12,
            'k': 13,
            'a': 14,
        }
        if card not in mapping:
            raise ValueError("Invalid input.")
        return mapping[card]

    def calculate_count(self):
        dealer_cards = self.parse_cards(self.dealer_entry.text())
        player_cards = self.parse_cards(self.player_entry.text())
        cards = dealer_cards + player_cards

        if any(c == 'exit' for c in cards):
            sys.exit()

        try:
            for card in cards:
                value = self.get_card_value(card)
                self.running_count = self.calculate_running_count(value, self.running_count)

            self.cards_played += len(cards)
            remaining_decks = (self.total_cards - self.cards_played) / self.cards_per_deck
            true_count = self.calculate_true_count(self.running_count, remaining_decks)

            self.result_label.setText(
                f'Running Count: {self.running_count}\nTrue Count: {true_count:.2f}'
            )
            self.update_advice(true_count)
        except ValueError as e:
            self.result_label.setText(str(e))

        self.dealer_entry.clear()
        self.player_entry.clear()

    def calculate_running_count(self, card_value, count):
        if 2 <= card_value <= 6:
            return count + 1
        elif card_value in [7, 8, 9]:
            return count
        elif 10 <= card_value <= 14:
            return count - 1
        else:
            raise ValueError("Invalid card value.")

    def calculate_true_count(self, running_count, remaining_decks):
        return running_count / remaining_decks

    def update_advice(self, true_count):
        if true_count >= 2:
            advice = "Bet more."
            self.red_card_image.setPixmap(QPixmap("red_card.png"))
            self.black_card_image.clear()
        elif 1 <= true_count < 2:
            advice = "Bet normal."
            self.black_card_image.setPixmap(QPixmap("black_card.png"))
            self.red_card_image.clear()
        elif 0 <= true_count < 1:
            advice = "Bet less. Deck is neutral."
            self.black_card_image.clear()
            self.red_card_image.clear()
        else:
            advice = "Bet the minimum. Count is negative."
            self.black_card_image.clear()
            self.red_card_image.clear()
        self.advice_label.setText(advice)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CardCountingApp()
    sys.exit(app.exec_())
