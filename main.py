from onr_tactile_interface import *
from onr_introduction_screen import *

import random


# the next three constants hold all the data. They must be the same length and in the same order!
CSV_FILES = ["onr_video_data\\bomb_success_final.csv", "onr_video_data\\temp_poke_final.csv"]
VIDEO_FILES = ["onr_video_data\\bomb_succes_final.MP4", "onr_video_data\\temp_poke_final.MP4"]
VIDEO_IDS = ["bomb_success", "temp_poke"]
NUM_TESTS = len(VIDEO_IDS)
NUM_REPEATS = 1
 

"""
This class hold a single set of data (csv file, video ID, and vid file)
"""
class Data():
    def __init__(self, csvFile, videoFile, vidId):
        self.csvFile = csvFile
        self.videoFile = videoFile
        self.vidId = vidId



"""
The main class. It creates all objects and starts the program
"""
def main():

    # loads all data and apps for screen 2
    dataList = []
    apps = []
    for i in range(NUM_TESTS):
        for j in range(NUM_REPEATS):
            dataList.append(Data(CSV_FILES[i], VIDEO_FILES[i], VIDEO_IDS[i])) # adds each video to the testing list 3 times
            apps.append(QApplication([])) # creats an app for each video

    random.shuffle(dataList) # randomizes order of videos

    postApp = QApplication([])

    # creates app 1
    app1 = QApplication([])

    # creates intro view/controller 
    introWindow = Window()
    introWindow.show()

    introController = Controller(introWindow)

    finishApp1 = app1.exec_()

    # the functionality to run one window after another closes was taken from this Stack Overflow question: https://stackoverflow.com/questions/72557224/close-current-window-and-open-new-one-in-conditions-pyqt
    for app in apps:
        if True: # if app1 is closed, run app(n)
            i = apps.index(app)
            print("Test " + str(i)) 

            # creates tactile model/view/controller
            tiWindow = InterfaceWindow()
            tiWindow.show()

            mySensorArray = SensorArray()

            tiController = InterfaceController(tiWindow, mySensorArray, dataList[i].csvFile, dataList[i].videoFile, dataList[i].vidId, i+1)

            finishApp2 = app.exec_()

    else:
        handleFinish = finishApp1

    sys.exit(handleFinish)

if __name__ == "__main__":
    main()