class Cardmodel():
    """The Model which represents the entire deck structure

    Attributes:
        cardCount: the exact number of different cards being printed
        cardHowOften: a list containing the numbers of time a card is supposed to be printed
        imgPaths: a list containing the paths of each of the cards which is supposd to be printed
        defaultImage: the path to the default image
    """
    def __init__(self):
        """
        Constructor of the Cardmodel
        Takes care of initialization.
        """
        self.cardCount = 0
        self.cardHowOften = []
        self.imgPaths = []
        self.defaultImage = "noCard.jpg"

    def addCard(self):
        """
        Adds a card to the model.
        """
        self.cardCount += 1
        self.cardHowOften.append(0)
        self.imgPaths.append(self.defaultImage)

    def deleteCard(self, i):
        """Deletes A card from the model at index i.
        Args:
            i: index of the card which is to be deleted
        """
        self.cardCount -= 1
        if self.cardCount > i:
            for j in range(i, self.cardCount):
                self.cardHowOften[j]=self.cardHowOften[j+1]
                self.imgPaths[j]=self.imgPaths[j+1]
        self.cardHowOften[self.cardCount] = 0
        self.imgPaths[self.cardCount] = self.defaultImage

    def resetCardCount(self):
        """resets the cardCount"""
        self.cardCount = 0

    def incrCardHowOften(self, i):
        """Increases number of cards to be printed
        Args:
            i: position of card
        """
        self.cardHowOften[i] += 1
        print self.cardHowOften[i]

    def decrCardHowOften(self, i):
        """Decreases number of cards to be printed if that number is higher than 0
        Args:
            i: position of card
        """
        if self.cardHowOften[i] > 0:
            self.cardHowOften[i] -= 1
        print self.cardHowOften[i]

    def incrCardCount(self):
        """Increases the Card count"""
        self.cardCount += 1

    def decrCardCount(self):
        """Decreases the Card count"""
        self.cardCount -= 1

    def appendCardHowOften(self):
        """Appends a card"""
        self.cardHowOften.append(0)

    def setImg(self, path, i):
        """Sets image of a card
        Args:
            path: path to new image
            i: index of card
        """
        self.imgPaths[i] = path

    def appendImg(self, path):
        """Creates new image in the list
        Args:
            path: path to image
        """
        self.imgPaths.append(path)

    #getter and setters

    def getImgPaths(self):
        return self.imgPaths

    def getCardCount(self):
        return self.cardCount

    def getImg(self, i):
        return self.imgPaths[i]

    def setCardHowOften(self, i, howOften):
        self.cardHowOften[i] = howOften

    def getCardHowOften(self):
        return self.cardHowOften

    def getCardHowOftenAt(self, i):
        return self.cardHowOften[i]

    def getCardCount(self):
        return self.cardCount