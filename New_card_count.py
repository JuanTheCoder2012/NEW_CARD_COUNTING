def calculate_running_count(card_value, count):
    if 2 <= card_value <= 6:
        return count + 1
    elif card_value in [7, 8, 9]:
        return count # 7, 8, and 9 are treated as 0 in the Hi-Lo system
    elif 10 <= card_value <= 13:
        return count - 1
    else:
        return count

def calculate_true_count(running_count, remaining_decks):
    return running_count / remaining_decks

def advise_bet(true_count):
    if true_count >= 2:
        return "Bet more."
    elif 1 <= true_count < 2:
        return "Bet normal."
    else:
        return "Bet less."

def main():
    decks = 8
    cards_per_deck = 52
    total_cards = decks * cards_per_deck
    running_count = 0  # Declare running_count outside the while loop

    print("Welcome to the 8-deck card counting game!")
    print("Enter card values (2-10, J, Q, K, A). Type 'exit' to quit.")

    while True:
        card_input = input("Enter a card value: ").strip().lower()

        if card_input == 'exit':
            break

        if card_input in ['2', '3', '4', '5', '6']:
            card_value = int(card_input)
        elif card_input in ['10', 'j', 'q', 'k', 'a']:
            card_value = 10
        elif card_input in ['7', '8', '9']:
            card_value = 0 #7, 8, and 9 are treated as 0 in the Hi-Lo system
        else:
            print("Invalid input. Please enter a valid card value.")
            continue

        running_count = calculate_running_count(card_value, running_count)
        remaining_decks = (total_cards - len(card_input.split())) / cards_per_deck
        true_count = calculate_true_count(running_count, remaining_decks)

        print(f"Running Count: {running_count}")
        print(f"True Count: {true_count:.2f}")
        print(advise_bet(true_count))

if __name__ == "__main__":
    main()
