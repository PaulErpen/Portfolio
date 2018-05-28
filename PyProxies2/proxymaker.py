from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from StringIO import StringIO


def placeCard(cardCount, imgPath, samples):
    """
    This function places a card based on the current count of cards on the appropriate page and position.

    Args:
        cardCount: the number of cards that have already been printed
        imgPath: a string which is the path of the image, which is supposed to be printed
        samples: a list of all pages, which have already been created
    """
    #special vars for placement
    xCoords = [27, 209, 390]
    yCoords = [569, 305, 45]
    sample = getCurrentSample(cardCount, samples)

    # Using ReportLab to insert image into PDF
    imgTemp = StringIO()
    imgDoc = canvas.Canvas(imgTemp)

    factor = 0.96
    # imgDoc.drawImage(imgPath, 208, 68, 177*factor, 250*factor)    ## at (399,760) with size 160x160
    imgDoc.drawImage(imgPath, xCoords[ cardCount % 3], yCoords [ cardCount % 9 / 3], 177 * factor, 250 * factor)  ## at (399,760) with size 160x160
    imgDoc.save()

    # Use PyPDF to merge the image-PDF into the template
    overlay = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
    sample.mergePage(overlay)


def getCurrentSample(cardCount, samples):
    """
    This function returns the sample which is being supposed to be written on based on the number of cards printed.
    It also takes care of creating a new page if need be.

    Args:
        cardCount: the number of cards that have already been printed
        samples: a list of all pages, which have already been created

    Returns:
        The sample, which is supposed to be printed on.
    """
    if(cardCount % 9 == 0):
        sample = PdfFileReader(file("pyProxiesSample.pdf", "rb")).getPage(0)
        samples.append(sample)
    return samples[cardCount / 9]


def writePdfFile(samples):
    """
    This function takes the pages and prints them into a default location.

    Args:
        samples: a list of all pages, which have already been created
    """
    # Save the result
    output = PdfFileWriter()

    for s in samples:
        output.addPage(s)

    output.write(file("output.pdf", "wb"))


def writePdfFileTo(samples,path):
    """
    This function takes the pages and prints them into a custom location.

    Args:
        samples: a list of all pages, which have already been created
        path: the path the PDF is supposed to be exported to
    """
    # Save the result
    output = PdfFileWriter()

    for s in samples:
        output.addPage(s)

    output.write(file(path, "wb"))


def writeData(cardNum,imgPaths,cardHowOften,writePath):
    """
    The function, which takes in a model and invokes the writePdfFileTo

    Args:
        cardNum: the number of different cards which are supposed to be printed
        imgPaths: a list of all the paths to the images
        cardHowOften: a list of numbers, which say how often a card is supposed to be printed
        writePath: the path where the PDF is supposed to be exported to
    """
    overallCount = 0
    samples = []
    for i in range(cardNum):
        print "i: "+str(i)
        path = imgPaths[i]
        cardTimes = cardHowOften[i]
        for j in range(cardTimes):
            print "j: " + str(j)
            placeCard(overallCount, path, samples)
            overallCount = overallCount + 1

    writePdfFileTo(samples,writePath)
