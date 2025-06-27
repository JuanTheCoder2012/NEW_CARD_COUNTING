import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
)
from PyQt5.QtGui import QPixmap

# Hi-Lo mapping for card counting
CARD_VALUES = {
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': -1,
    'j': -1,
    'q': -1,
    'k': -1,
    'a': -1,
}

class CardCountingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.running_count = 0
        self.cards_per_deck = 52
        self.cards_played = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Card Counting')

        deck_label = QLabel('Number of decks:')
        self.deck_input = QSpinBox(self)
        self.deck_input.setRange(1, 8)
        self.deck_input.setValue(8)

        deck_layout = QHBoxLayout()
        deck_layout.addWidget(deck_label)
        deck_layout.addWidget(self.deck_input)

        self.label = QLabel('Enter card values (2-10, J, Q, K, A) separated by spaces:')
        self.entry = QLineEdit(self)
        self.result_label = QLabel(self)
        self.advice_label = QLabel(self)
        self.red_card_image = QLabel(self)
        self.black_card_image = QLabel(self)

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate_count)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_count)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.exit_button)

        layout = QVBoxLayout(self)
        layout.addLayout(deck_layout)
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.advice_label)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.red_card_image)
        images_layout.addWidget(self.black_card_image)
        layout.addLayout(images_layout)

        self.show()

    @property
    def total_cards(self):
        return self.deck_input.value() * self.cards_per_deck

    def calculate_count(self):
        card_input = self.entry.text().strip().lower()
        if not card_input:
            return
        if card_input == 'exit':
            self.close()
            return

        cards = card_input.split()
        for card in cards:
            value = CARD_VALUES.get(card)
            if value is None:
                self.result_label.setText(f'Invalid input: {card}')
                self.entry.clear()
                return
            self.running_count += value
            self.cards_played += 1

        remaining_decks = (self.total_cards - self.cards_played) / self.cards_per_deck
        remaining_decks = max(remaining_decks, 0.1)
        true_count = self.running_count / remaining_decks

        self.result_label.setText(
            f'Running Count: {self.running_count}\nTrue Count: {true_count:.2f}'
        )
        self.update_advice(true_count)
        self.entry.clear()

    def reset_count(self):
        self.running_count = 0
        self.cards_played = 0
        self.result_label.clear()
        self.advice_label.clear()
        self.red_card_image.clear()
        self.black_card_image.clear()

    def update_advice(self, true_count: float):
        if true_count >= 2:
            advice = 'Bet more.'
            self.red_card_image.setPixmap(QPixmap('red_card.png'))
            self.black_card_image.clear()
        elif 1 <= true_count < 2:
            advice = 'Bet normal.'
            self.black_card_image.setPixmap(QPixmap('black_card.png'))
            self.red_card_image.clear()
        else:
            advice = 'Bet less.'
            self.black_card_image.clear()
            self.red_card_image.clear()
        self.advice_label.setText(advice)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CardCountingApp()
    sys.exit(app.exec_())
