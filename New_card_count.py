import tkinter as tk

class CardCountingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Card Counting")
        
        self.running_count = 0
        self.decks = 8
        self.cards_per_deck = 52
        self.total_cards = self.decks * self.cards_per_deck
        
        self.label = tk.Label(master, text="Enter card values (2-10, J, Q, K, A, 7, 8, 9). Type 'exit' to quit:")
        self.label.pack()
        
        self.entry = tk.Entry(master)
        self.entry.pack()
        
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()
        
        self.advice_label = tk.Label(master, text="")
        self.advice_label.pack()
        
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate_count)
        self.calculate_button.pack()
        
        self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy)
        self.exit_button.pack()
    
    def calculate_count(self):
        card_input = self.entry.get().strip().lower()
        
        if card_input == 'exit':
            self.master.destroy()
            return
        
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
            
            self.result_label.config(text=f"Running Count: {self.running_count}\nTrue Count: {true_count:.2f}")
            self.update_advice(true_count)
        except ValueError as e:
            self.result_label.config(text=str(e))
            
        # Clear the input field after calculation
        self.entry.delete(0, tk.END)    
    
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
        elif 1 <= true_count < 2:
            advice = "Bet normal."
        else:
            advice = "Bet less."
        self.advice_label.config(text=advice)

if __name__ == "__main__":
    root = tk.Tk()
    app = CardCountingApp(root)
    root.mainloop()
