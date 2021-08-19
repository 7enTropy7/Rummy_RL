import pydealer

deck = pydealer.Deck()

deck.shuffle()
cards = deck.deal(10)

print(deck.size)