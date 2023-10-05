import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
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

        self.label = QLabel('Enter card values (2-10, J, Q, K, A, 7, 8, 9). Type "exit" to quit:')
        self.entry = QLineEdit(self)
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

    def calculate_count(self):
        card_input = self.entry.text().strip().lower()

        if card_input == 'exit':
            sys.exit()

        try:
            if card_input in ['2', '3', '4', '5', '6']:
                card_value = int(card_input)
            elif card_input in ['10', 'j', 'q', 'k', 'a']:
                card_value = 10
            elif card_input in ['7', '8', '9']:
                card_value = 0
            else:
                raise ValueError("Invalid input.")

            self.running_count = self.calculate_running_count(card_value, self.running_count)
            remaining_decks = (self.total_cards - len(card_input.split())) / self.cards_per_deck
            true_count = self.calculate_true_count(self.running_count, remaining_decks)

            self.result_label.setText(f'Running Count: {self.running_count}\nTrue Count: {true_count:.2f}')
            self.update_advice(true_count)
        except ValueError as e:
            self.result_label.setText(str(e))

        self.entry.clear()

    def calculate_running_count(self, card_value, count):
        if 2 <= card_value <= 6:
            return count + 1
        elif card_value in [7, 8, 9]:
            return count
        elif 10 <= card_value <= 13:
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
        else:
            advice = "Bet less."
            self.black_card_image.clear()
            self.red_card_image.clear()
        self.advice_label.setText(advice)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CardCountingApp()
    sys.exit(app.exec_())
