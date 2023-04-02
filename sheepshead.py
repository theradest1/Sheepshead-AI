import random

#card config:
cardTitles = ["7", "8", "9", "king", "10", "ace", "jack", "queen"]
cardPoints = [0, 0, 0, 4, 10, 11, 2, 3]
cardSuits = ["diamonds", "hearts", "spades", "clubs"]
cards = []
blind = []
#playedCards = [] #will add this later

#game config:
players = []
totalPlayers = 5
leadPlayer = 0

#setup
class player:
	def __init__(self, playerPos):
		self.playerPos = playerPos
		self.cardList = []
		self.team = ""
		self.points = 0

	def addCard(self, card):
		self.cardList.append(card)
        
	def addPoints(self, points):
		self.points += points
	def playCard(self):
		return self.cardList.pop(random.randint(0, len(self.cardList) - 1))
	def lead(self):
		return self.cardList.pop(random.randint(0, len(self.cardList) - 1))
		

for i in range(totalPlayers):
    players.append(player(1))



#game  --------------------------
def deal():
	global cardSuits, cardTitles, totalPlayers, players
	blind = []
	deck = []
	for titleID in range(len(cardTitles)):
		for suitID in range(len(cardSuits)):
			deck.append(titleID + suitID /10)
			#print(card + " of " + suit + " is worth " + str(cardPoints[index]))
	totalCards = len(deck)
	cardsInBlind = totalCards%totalPlayers
	shuffle(deck, 1) #3 is just a random number that sounds about right
	for cardID in range(int((len(deck) - cardsInBlind)/totalPlayers)):
		for playerID in range(len(players)):
			players[playerID].addCard(deck[cardID + (totalPlayers + 1)*playerID])
	return deck[-cardsInBlind:], deck
	

def shuffle(deck, iterations):
    for i in range(iterations):
        for cardIndex in range(len(deck)):
            randomIndex = random.randint(0, len(deck) - 1)
            temp = deck[cardIndex]
            deck[cardIndex] = deck[randomIndex]
            deck[randomIndex] = temp
    return deck
	
def playRound():
	global players
	playedCards = []
	playedCards.append(players[leadPlayer].lead())
	for playerID in range(len(players) - 1):
		playedCards.append(players[(playerID + leadPlayer + 1)%(totalPlayers)].playCard())
	
	roundWinner = winnerOfRound(playedCards)
	players[roundWinner].addPoints(countPoints(playedCards))
	return roundWinner

def winnerOfRound(playedCards):
    biggestCard = playedCards[1]
    for card in playedCards:
        if round(card) >= 6 or (card - round(card)) * 10 == 0: #if is trump
            if card > biggestCard:
                biggestCard = card
        elif (card - round(card)) * 10 == (biggestCard - round(biggestCard)) * 10:
            if card > biggestCard:
                biggestCard = card
    return playedCards.index(biggestCard)

def countPoints(playedCards):
	global cardPoints
	points = 0
	for card in playedCards:
		points += cardPoints[round(card)]
	print("Round had " + str(points) + " points")
	return points

def playHand():
	blind, cards = deal()
	roundNum = 0
	print("Delt Cards -----------------------")
	print("Blind: " + str(blind))
	for playerID in range(len(players)):
		print("Player " + str(playerID) + ": " + str(players[playerID].cardList))

	while len(players[0].cardList) > 0:
		roundNum += 1
		print("Round " + str(roundNum) + " -----------------------")
		leadPlayer = playRound()
		for playerID in range(len(players)):
			print("Player " + str(playerID) + ": " + str(players[playerID].cardList) + " Points: " + str(players[playerID].points))


playHand()
