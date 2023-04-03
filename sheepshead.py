import random

#card config:
cardTitles = ["7", "8", "9", "king", "10", "ace", "jack", "queen"]
cardPoints = [0, 0, 0, 4, 10, 11, 2, 3]
cardSuits = ["diamonds", "hearts", "spades", "clubs"]
blind = []
#playedCards = [] #will add this later

#game config:
players = []
totalPlayers = 5

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
	def playCard(self, roundCards):
		#data that is known: all currently played cards, your playable cards


		#get playable cards
		playableCards = []
		ledSuit = int((roundCards[0] - int(roundCards[0])) * 10)
		for cardID in range(len(self.cardList)):
			if int((cardID - int(cardID)) * 10) == ledSuit:
				playableCards.append(self.cardList[cardID])
		if len(playableCards) == 0:
			playableCards = self.cardList

		if self.playerPos == 0:
			#AI stuffs
			playedCard = playableCards[random.randint(0, len(playableCards) - 1)]
			self.cardList.remove(playedCard)
			return playedCard

		playedCard = playableCards[random.randint(0, len(playableCards) - 1)]
		self.cardList.remove(playedCard)
		return playedCard
	
	def lead(self):
		if self.playerPos == 0:
			#AI stuffs
			return self.cardList.pop(random.randint(0, len(self.cardList) - 1))	

		return self.cardList.pop(random.randint(0, len(self.cardList) - 1))

for i in range(totalPlayers):
    players.append(player(i))



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
	return deck[-cardsInBlind:]
	

def shuffle(deck, iterations):
    for i in range(iterations):
        for cardIndex in range(len(deck)):
            randomIndex = random.randint(0, len(deck) - 1)
            temp = deck[cardIndex]
            deck[cardIndex] = deck[randomIndex]
            deck[randomIndex] = temp
    return deck
	
def playRound(leadPlayer):
	global players
	playedCards = []
	playedCards.append(players[leadPlayer].lead())
	print("Player " + str(leadPlayer) + " led the " + cardIDToName(playedCards[-1]))
	for playerID in range(1, len(players)):
		playedCards.append(players[(playerID + leadPlayer)%totalPlayers].playCard(playedCards))
		print("Player " + str((playerID + leadPlayer)%totalPlayers) + " played " + cardIDToName(playedCards[-1]))
	
	roundWinner = (winnerOfRound(playedCards) + leadPlayer)%totalPlayers
	print("Player " + str(roundWinner) + " won the round")
	players[roundWinner].addPoints(countPoints(playedCards))
	return roundWinner, playedCards

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

def cardIDToName(cardID):
    global cardSuits, cardTitles
    return cardTitles[int(cardID)] + " of " + cardSuits[int((cardID - int(cardID)) * 10)]

def cardListToNames(cardList):
    finalNames = ""
    for cardID in cardList:
        finalNames += cardIDToName(cardID) + ", "
    return finalNames[:-2]

def playHand():
	leadPlayer = 0
	blind = deal()
	roundNum = 0
	handPlayedCards = []
	print("Delt Cards -----------------------")
	print("Blind: " + cardListToNames(blind))
	for playerID in range(len(players)):
		print("Player " + str(playerID) + ": " + cardListToNames((players[playerID].cardList)))

	while len(players[0].cardList) > 0:
		roundNum += 1
		print("Round " + str(roundNum) + " -----------------------")
		leadPlayer, playedCards = playRound(leadPlayer)
		handPlayedCards += playedCards
		for playerID in range(len(players)):
			print("Player " + str(playerID) + ": " + cardListToNames((players[playerID].cardList)) + "     Points: " + str(players[playerID].points))

playHand()