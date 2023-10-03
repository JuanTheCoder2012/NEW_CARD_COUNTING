NUM_ON_CARDS= {
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    '6': 1,
    '7': 0,
    '8': 0,
    '9': 0,
    '0': -1,
    'J': -1,
    'Q': -1,
    'K': -1,
    'A': -1,
}
deck = 8
def main():
    while True:
        inp = input('Enter a card or "exit" to quit')
        if inp.lower() == 'exit':
            break
        elif not inp:
            continue
        cards = len(inp)
        count = 0 
        for card in inp:
            count += NUM_ON_CARDS.get(card.upper(), 0)
            played = cards / 52.0
            truecount = count / (deck - played)
        print('Count: {}'.format(count))
        print('True count: {}'.format(truecount))
if __name__ == '__main__':
    main()
    
    