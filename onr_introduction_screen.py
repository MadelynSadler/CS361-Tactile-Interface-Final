import sys, zmq, json

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
QFormLayout, QLineEdit, QScrollArea, QMessageBox)

INSTRUCTIONS1 = ("<html>Imagine you are supervising a robot that is attempting to autonomously pick up objects" +
                 " underwater. The robot is still learning the best way to pick up objects. Your role as " +
                 "supervisor is to <u>monitor the robot and tell it to stop when the attempt to pick up the " +
                 "object has failed.</u> <br><br>" +
                 "To determine whether the robot's grasp attempt is succeeding or failing, " +
                 "you will need to monitor real-time tactile information from the robot gripper. A " +
                 "visualization of the gripper's two \"finger pads\" will show you when the robot is making " +
                 "contact with the object, and the force of the contact: on a continuum of light gray " +
                 "(light touch) to black (forceful touch).</html>")
INSTRUCTIONS2 = "Here is an example of what you would see if the robot\'s left finger is firmly touching an object with the whole tip of the finger pad."
INSTRUCTIONS3 = ("<html>The robot also has a live camera feed, but because the water is murky it is impossible to tell " +
                 "from the camera alone whether an attempt to pick up an object is failing/succeeding. <br><br>" +
                 "<b>Therefore, it is critical that you pay close attention to the tactile information in order " +
                 "to make the correct judgment about the grasp attempt.</b></html>")
INSTRUCTIONS4 = ("<html><b>IMPORTANT</b> - Each robot grasp attempt is very costly in terms of battery life. You should " +
                 "stop a failing grasp as soon as possible! <br><br>" +
                 "It is expected that the robot will sometimes fail " +
                 "to pick up the object. <u>Your primary goal as supervisor is to identify failing grasps early " +
                 "so that robot battery life is preserved for future grasp attempts.</u>" + 
                 "<ul><li>If you think the grasp attempt is <u>failing</u>, <b>press STOP</b>.</li>" +
                 "<li>If you think the grasp attempt is <u>succeeding</u>, <b>do nothing</b> (let the robot continue picking up the object)</li></ul></html>")
INSTRUCTIONS5 = ("<html>Following each grasp attempt you will be asked to make a confidence judgment, using a scale of 1 (Very Confident) to 5 (Very Unconfident)" +
                 "<ul><li><u>If you pressed STOP</u>, how confident are you that the grasp attempt would have failed?</li>" +
                 "<li><u>If you did nothing</u>, how confident are you that the grasp attempt was successful?</li></ul>" + 
                 "<b>Once you have made your confidence judgment you will have 3 seconds before the next grasp attempt begins.</b></html>")
INSTRUCTIONS6 = ("<html><b><u>Tell the experimenter you are ready to begin.</b></u><br>" +
                 "Once you have received confirmation from the experimenter, click OK to see the first grasp attempt.\n" +
                 "You will see 36 total attempts.</html>")

INSTRUCTIONS_LIST = [INSTRUCTIONS1, INSTRUCTIONS2, INSTRUCTIONS3, INSTRUCTIONS4, INSTRUCTIONS5, INSTRUCTIONS6]
IMAGE_LIST = ["instruction_images\\gripper_img1.png","instruction_images\\gripper_img2.png", "instruction_images\\distorted_video.png", "instruction_images\\interface.png"]



# this class was created partly with a GeeksForGeeks tutorial found here: https://www.geeksforgeeks.org/pyqt5-scrollable-label/ 
class ScrollLabel(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)

        self.content = QWidget(self)
        self.setWidget(self.content)

        self.layout = QHBoxLayout(self.content)
        self.textLayout = QVBoxLayout()
        self.imageLayout = QVBoxLayout()
        self.layout.addLayout(self.textLayout)
        self.layout.addLayout(self.imageLayout)

    
    # adds given text to the scrollable widget
    def addText(self, text):
        label = QLabel(self.content)
        label.setWordWrap(True)
        label.setText(text)
        label.setFont(QFont('Arial', 15))
        self.textLayout.addWidget(label, alignment=Qt.AlignCenter)

    # adds given image from file to the center of the scrollLable widget
    def addImage(self, file):
        gripperImg = QLabel()
        gripperImg.setAlignment(Qt.AlignCenter)
        gripperImg.setPixmap(QtGui.QPixmap(file).scaled(600, 800, Qt.KeepAspectRatio))
        self.imageLayout.addWidget(gripperImg)
    
    # this clears all items in a layout
    def clearLayout(self):
        while self.textLayout.count():
            child = self.textLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        while self.imageLayout.count():
            child = self.imageLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()



class IdWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # window stuff
        self.setWindowTitle("Participant ID")
        self.setFixedHeight(200)
        self.setFixedWidth(700)
        self.setWindowModality(QtCore.Qt.ApplicationModal) # makes IdWindow a modal, meaning it freezes interaction with the window that calls it until it is closed

        # layouts
        outerLayout = QVBoxLayout()
        idLayout = QFormLayout()

        # id stuff
        self.idBox = QLineEdit()
        self.idBox.setAlignment(Qt.AlignLeft)
        self.idBox.setFont(QFont("Arial", 18))
        self.idBox.setFixedWidth(300)

        # button
        self.submitButton= QPushButton("Submit")
        self.submitButton.setFixedSize(200, 60)
        self.submitButton.setFont(QFont('Arial', 15))

        # fill form
        idLayout.addRow("Participant ID: ", self.idBox)
        idLayout.labelForField(self.idBox).setFont(QFont("Arial", 18)) # sets label font

        # pull it all together
        outerLayout.addLayout(idLayout)
        outerLayout.addWidget(self.submitButton, alignment=Qt.AlignRight)

        centralWidget = QWidget(self)
        centralWidget.setLayout(outerLayout)
        self.setCentralWidget(centralWidget)



class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # window stuff
        self.setWindowTitle("Study Introduction")
        self.setFixedHeight(950)
        self.setFixedWidth(1200)

        # layouts and things
        outerLayout = QVBoxLayout()
        buttonsLayout = QHBoxLayout()
        descriptionLayout = QVBoxLayout()

        # next
        self.nextButton = QPushButton("Next")
        self.nextButton.setFixedSize(200, 60)
        self.nextButton.setFont(QFont('Arial', 15))

        # back
        self.backButton = QPushButton("Back")
        self.backButton.setFixedSize(200, 60)
        self.backButton.setFont(QFont('Arial', 15))

        # create all scroll labels
        self.instructionsLabel = (ScrollLabel(self))    
        self.instructionsLabel.addText(INSTRUCTIONS_LIST[0])
        self.instructionsLabel.addImage(IMAGE_LIST[0])

        descriptionLayout.addWidget(self.instructionsLabel)

        # pull it all together
        buttonsLayout.addWidget(self.backButton, alignment=Qt.AlignRight)
        buttonsLayout.addWidget(self.nextButton, alignment=Qt.AlignRight)

        outerLayout.addLayout(descriptionLayout)    
        outerLayout.addLayout(buttonsLayout)

        centralWidget = QWidget(self)
        centralWidget.setLayout(outerLayout)
        self.setCentralWidget(centralWidget)


    def clearInstructions(self):
        self.instructionsLabel.clearLayout()
    
    def changePage(self, page):
        self.instructionsLabel.addText(INSTRUCTIONS_LIST[page])
        if page < len(IMAGE_LIST): # add image if there is an image for that page
            self.instructionsLabel.addImage(IMAGE_LIST[page])



class Controller:

    def __init__(self, view):
        self.view = view
        self.currScreen = 0
        self.view.nextButton.clicked.connect(self._nextClicked)
        self.view.backButton.clicked.connect(self._backClicked)

        # pull up ID Window
        self.popUp = IdWindow()
        self.popUp.show()
        self.popUp.submitButton.clicked.connect(self._submitClicked)
        self.instructionPage = 0

        
    def _nextClicked(self):
        self.view.clearInstructions()
        if self.instructionPage == len(INSTRUCTIONS_LIST)-1: # if that's the last page of instructions
            self.view.close()
        else:
            if self.instructionPage == len(INSTRUCTIONS_LIST) - 2: # change next button to "ok"
                self.view.nextButton.setText("OK")
            self.instructionPage += 1
            self.view.changePage(self.instructionPage)

    
    def _backClicked(self):
        if self.instructionPage != 0: # if the first instruction isn't already displaying
            if self.instructionPage != len(INSTRUCTIONS_LIST) - 2: # change "ok" to "next"
                self.view.nextButton.setText("Next")
            self.view.clearInstructions()
            self.instructionPage -= 1
            self.view.changePage(self.instructionPage)


    def _submitClicked(self):
        if self.popUp.idBox.text() == "":
            err = QMessageBox()
            err.setText("Participant ID can not be left blank.")
            err.setWindowTitle("Error")
            err.exec_()
        else:
            if self._testMicroservice() != "invalid":
                open('participant_data\\participant_id.txt', 'w').close()
                with open("participant_data\\participant_id.txt", 'w') as file:
                    file.write(self.popUp.idBox.text())
                # creates file named participant_id.csv and writes headers
                with open("participant_data\\" + str(self.popUp.idBox.text()) + ".csv", "a") as file:
                    file.write("TestNumber, VideoID, StoppedClicked, TimeElapsed, Confidence, HowEasyToDetermineSuccessfulGrasps, HowImportantTactileInformation, HowImportantCameraFeed, FreeResponse\n")
                self.popUp.close()


    def _testMicroservice(self):

        context = zmq.Context()

        #  Socket to talk to server
        print("Connecting to validation microservice...")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        socket.send_string(self.popUp.idBox.text())
        print("Request sent")

        #  Get the reply.
        message = socket.recv_string()
        print(f"Received reply [ {message} ]")
        return message


def main():
    introApp = QApplication([])
    introWindow = Window()
    introWindow.show()

    introController = Controller(introWindow)

    sys.exit(introApp.exec())



if __name__ == "__main__":
    main()