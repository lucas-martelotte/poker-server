import os

card_path = 'data/resources/img/cards/'

for card_name in os.listdir(card_path):
    try:
        card_parts = card_name.split('.')[0].split('_')
        number = card_parts[0]
        suit = card_parts[len(card_parts)-1]

        has_2 = False
        if suit.endswith('2'):
            suit = suit[:-1]
            has_2 = True


        if number == 'jack':
            number = '11'
            if not has_2:
                os.remove(card_path + card_name)
        elif number == 'queen':
            number = '12'
            if not has_2:
                os.remove(card_path + card_name)
        elif number == 'king':
            number = '13'
            if not has_2:
                os.remove(card_path + card_name)
        elif number == 'ace':
            number = '1'

        if suit == 'spades':
            suit = 's'
        elif suit == 'diamonds':
            suit = 'd'
        elif suit == 'hearts':
            suit = 'h'
        elif suit == 'clubs':
            suit = 'c'

        os.rename(card_path + card_name, card_path + number + suit + '.png')
    except:
        pass