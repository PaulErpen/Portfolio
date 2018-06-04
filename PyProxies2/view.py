from Tkinter import Label, Tk, Frame, Canvas, Scrollbar, GROOVE, Button
import tkSimpleDialog
import tkFileDialog
from PIL import Image, ImageTk
from os.path import expanduser
import os
from cardmodel import Cardmodel
import proxymaker

class MtgProxyView(Frame):
    """The View, which takes care of the visual representation of the model.

    Attributes:
        root: the root panel for the visual represantion
        cardModel: the cardModel class which deals with all the internal card data
        home: the path of where images are located
        safeHome: the path where PDfs are supposed to be saved
        cnfData: the path to the config file
        defaultImage: the path to the default image
        listFrame: the frame in which the mode is portraied
        canvas: tha canvas which allows scrolling and a grid
        myscrollbar: the scrollbar which gives the user the abilty to scroll through the list of cards
        buttonframe: the frame in which the action buttons are being placed
        wipeWorkspace: the button which corresponds with the clear worksapce function
        bSelectDir: the button which corresponds with the selectDir function
        selectSaveDir: the button which corresponds with the selectSaveDir function
        bMake: the button which corresponds with the makePdf function
        addButton: the button which corresponds with the addNewCard function
    """
    def __init__(self):
        """
        This is the the constructor of the MtgProxyView
        It takes care of all the setup and doesnt require anything from the main
        """
        #basic setup
        sizex = 765
        sizey = 525
        posx  = 0
        posy  = 0
        self.root = Tk()
        self.root.title("PyProxies")
        self.root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.root.resizable(width=False, height=False)

        #backend data setup
        self.cardmodel = Cardmodel()

        #constants
        self.home = ""
        self.safeHome = ""
        self.cnfData = "upm.cnf"
        self.defaultImage = "noCard.jpg"
        self.loadConfig()

        #list setup
        self.listframe=Frame(self.root,relief=GROOVE,width=500,height=500,bd=1)
        self.listframe.place(x=10,y=10)
        self.canvas=Canvas(self.listframe)
        self.frame=Frame(self.canvas)
        self.myscrollbar=Scrollbar(self.listframe,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        #and it scrollbar
        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')

        #button setup
        self.buttonframe=Frame(self.root, relief=GROOVE,width=100,height=500,bd=1,padx = 15, pady = 10)
        self.buttonframe.place(x=535, y=10)
        self.wipeWorkspace = Button(self.buttonframe, text="clear Workspace", command=self.completeWipe, width=20)
        self.wipeWorkspace.pack(anchor="sw", pady=5)
        self.bSelectDir = Button(self.buttonframe, text="select a fitting Directory", command=self.selectDir, width=20)
        self.bSelectDir.pack(anchor="sw",  pady=5)
        self.selectSaveDir = Button(self.buttonframe, text="Select a save directory", command=self.selectSafeDir, width=20)
        self.selectSaveDir.pack(anchor="sw",  pady=5)
        self.bMake = Button(self.buttonframe, text="make PDF", command=self.makePdf, width=20)
        self.bMake.pack(anchor="sw",  pady=5)
        self.addButton = Button(self.frame, text="add a new Card", command = self.addNewCard)

        self.frame.bind("<Configure>",self.myfunction)
        self.data()

        self.root.mainloop()

    def loadConfig(self):
        """
        This is the functions which loads the configuration.
        Only the place where Images can be added as sources and where PDFs can be saved,
        are able to be set and saved.
        """
        configFile = open(self.cnfData,"r+")
        temp = configFile.read().split("\n")
        try:
            self.home = expanduser("~")
            if os.path.exists(temp[0]):
                self.home = temp[0]
            self.safeHome = expanduser("~")
            if os.path.exists(temp[1]):
                self.safeHome = temp[1]
        except IndexError:
            print "Error"
            self.home = expanduser("~")
            self.safeHome = expanduser("~")
        print "new homes"
        print self.home
        print self.safeHome
        configFile.close()

    def saveConfig(self):
        """
        This Function takes care of writing the values of the home and the saveHome to the configuration file
        """
        configFile = open(self.cnfData, "w")
        configFile.write(self.home+"\n"+self.safeHome)
        print "config saved"
        configFile.close()
        self.loadConfig()

    def completeWipe(self):
        """
        This function clears the workspace of all of its components and resets the Model.
        """
        for i in range(self.cardmodel.getCardCount()):
            #self.cardHowOften[i]=0
            self.cardmodel.setCardHowOften(i, 0)
            self.cardmodel.setImg(self.defaultImage,i)
            #self.imgPaths[i] = self.defaultImage
        self.cardmodel.resetCardCount()
        for w in self.frame.winfo_children():
            w.destroy()
        self.data()

    def selectSafeDir(self):
        """
        This function sets the directory where exported PDFs are being stored.
        Its does this by invoking the tkFileDialog which asks for user input and returns a valid path.
        """
        path = tkFileDialog.askdirectory(initialdir = self.safeHome, title = "Select a better save directory.")
        if isinstance(path, basestring):
            self.safeHome = path
            self.saveConfig()

    def selectDir(self):
        """
        This function provides the user with the functionality to set their starting directory for adding source images.
        They can do this in order to save time and optimize their workflow.
        Its does this by invoking the tkFileDialog which asks for user input and returns a valid path.
        """
        path = tkFileDialog.askdirectory(initialdir = self.home, title = "Select a better working directory.")
        if isinstance(path,basestring):
            self.home = path
            self.saveConfig()

    def data(self):
        """
        The data function takes care of going over the entiry model and representing it on the canvas object.
        It is only supposed to be invoked when the workspace has been cleard beforehand.
        """
        for i in range(self.cardmodel.getCardCount()):
            #image label
            pilFile = Image.open(self.cardmodel.getImg(i))
            image1 = pilFile.resize((60, 80), Image.ANTIALIAS)
            image2 = ImageTk.PhotoImage(image1)
            imageLabel = Label(self.frame, image=image2)
            imageLabel.image = image2
            imageLabel.grid(row=i, column=0, padx=2, pady=2)
            #other labels
            Label(self.frame,text="Card is being printed "+str(self.cardmodel.getCardHowOftenAt(i))+" times.").grid(row=i, column=1)
            Button(self.frame, text="-", command=lambda i=i: self.decrHowOften(i)).grid(row=i, column=2)
            Button(self.frame, text="+", command=lambda i=i: self.incrHowOften(i)).grid(row=i, column=3)
            Button(self.frame, text="add Source", command=lambda i=i: self.getImgPath(i)).grid(row=i, column=4)
            Button(self.frame, text="X", command=lambda i=i: self.delete(i)).grid(row=i, column=5)

        self.addButton = Button(self.frame, text="add a new Card", command=self.addNewCard)
        self.addButton.grid(row=self.cardmodel.getCardCount(), column=0, columnspan=2, padx=10, pady=20, sticky="W")

    def updateOne(self,i):
        """
        This Function is supposed to only update one row of the Canvas in,
        which the model is displayed.

        Args:
            i: the index of the row which is supposed to be updated
        """
        pilFile = Image.open(self.cardmodel.getImg(i))
        image1 = pilFile.resize((60, 80), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image1)
        imageLabel = Label(self.frame, image=image2)
        imageLabel.image = image2
        imageLabel.grid(row=i, column=0, padx=2, pady=2)
        # other labels
        Label(self.frame, text="Card is being printed " + str(self.cardmodel.getCardHowOftenAt(i)) + " times.").grid(row=i, column=1)
        Button(self.frame, text="-", command=lambda i =i: self.decrHowOften(i)).grid(row=i, column=2)
        Button(self.frame, text="+", command=lambda i =i: self.incrHowOften(i)).grid(row=i, column=3)
        Button(self.frame, text="add Source", command=lambda i=i: self.getImgPath(i)).grid(row=i, column=4)
        Button(self.frame, text="X", command=lambda i =i: self.delete(i)).grid(row=i, column=5)

    def delete(self,i):
        """
        This function is supposed to delete one Card and update the model accordingly.

        Args:
            i: the indexing of the row, which is supposed to be updated
        """
        self.cardmodel.deleteCard(i)

        #complete reset
        for w in self.frame.winfo_children():
            w.destroy()
        self.data()

    def incrHowOften(self,i):
        """
        This function takes care of increasing the counter of how often a card is supposed to be printed.

        Args:
            i: the row in which the the card is located
        """
        self.cardmodel.incrCardHowOften(i)
        self.updateOne(i)

    def decrHowOften(self, i):
        """
        This function takes care of decreasing the counter of how often a card is supposed to be printed.

        Args:
            i: the row in which the the card is located
        """
        self.cardmodel.decrCardHowOften(i)
        self.updateOne(i)

    def addNewCard(self):
        """
        This function adds a new card to the model and updates it with default values.
        It then invokes the updateOne-function in order to update the view.
        """
        self.cardmodel.addCard()

        self.addButton.destroy()
        self.addButton = Button(self.frame, text="add a new Card", command = self.addNewCard)
        self.addButton.grid(row=self.cardmodel.getCardCount(), column = 0, columnspan = 2, padx = 10, pady= 20,sticky="W")

        self.updateOne(self.cardmodel.getCardCount()-1)

    def myfunction(self, event):
        """
        A function which is called in the event of a configuration concerning the frame.
        It sets the scrollregion of the scrollbar to be the canvas
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=500,height=500)

    def getImgPath(self, i):
        """
        This function allows the user to change the image source of a card.
        It does this by invoking the tkFileDialog in order to ask for a filename,
        limited to JPGs and PNGs.
        If the user input something it updates the model.

        Args:
            i: index of the row in which the card is located
        """
        imgPath = tkFileDialog.askopenfilenames(initialdir=self.home, title="Select Image",filetypes = [("JPG files","*.jpg"),("PNG files","*.png"),("JPEG files","*.jpeg")])
        print imgPath
        print str(imgPath) == "()"
        if str(imgPath) != "()" and str(imgPath) !="":
            print (imgPath[0])
            self.cardmodel.setImg(imgPath[0] ,i)
            self.updateOne(i)
        else:
            print "user didnt select anything"


    def makePdf(self):
        """
        This function gives the user the functionality to select a filename for the PDF they want to print.
        Afterwards if a name has been entered the function gives the model to the proxymaker module,
        which creates a PDF in the desired location.
        """
        name = tkSimpleDialog.askstring('Input','Enter the desired name for the PDF, without suffix')
        if name is not None:
            proxymaker.writeData(self.cardmodel, self.safeHome+"/"+name+".pdf")
