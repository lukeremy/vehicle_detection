import time
import sys
import _capture_init as cap_init

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from _help_init import HelpInit

# Interface Load
main_ui = uic.loadUiType("gtk/main.ui")[0]
help_ui = uic.loadUiType("gtk/help.ui")[0]

# Variable
fileLoc = None


class MainInit(QMainWindow, main_ui):
    def __init__(self, parent=None):
        # Initialization main interface from QT to Python
        QMainWindow.__init__(self, parent)

        # Variable
        self.setupUi(self)
        self.capture = None

        port_cam = ["", "0", "1", "2"]
        filename = None
        video_mode = None
        boundary = None
        roi = None
        alt = None
        elevated = None
        fps = None

        # Menu Bar
        # File
        self.actionExit.triggered.connect(self.file_exit)

        # 1.    Setting
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)

        # 1.1.  VideoInput
        self.radioButton_choseFile.setChecked(True)
        self.radioButton_choseDevice.setChecked(False)

        self.radioButton_choseFile.toggled.connect(self.radioChoseFile)
        self.radioButton_choseDevice.toggled.connect(self.radioChoseDevice)

        self.label_selectFile.setText('')
        self.pushButton_selectFile.clicked.connect(self.selectFile)

        self.comboBox_choseDevice.setEnabled(False)
        self.comboBox_choseDevice.addItems(port_cam)
        self.comboBox_choseDevice.currentIndexChanged.connect(self.selectionDevice)

        # 1.2.  VideoMode
        self.radioButton_rgbVM.setChecked(True)
        self.radioButton_gsVM.setChecked(False)
        self.radioButton_hsvVM.setChecked(False)
        self.radioButton_edVM.setChecked(False)
        self.checkBox_showboundaryVM.setChecked(False)
        self.checkBox_showroiVM.setChecked(False)

        # 1.3   Data Input
        # 1.3.1 Camera
        self.lineEdit_altitudeCam.setText(format("100"))
        self.lineEdit_elevatedCam.setText(format("30"))
        self.lineEdit_fps.setText(format(fps))

        # 1.3.2 SpeedDetection
        self.radioButton_EuclideanModel.setChecked(True)
        self.radioButton_PinHoleModel.setChecked(False)

        # 1.4 Button Help and Set
        self.pushButton_helpSetting.clicked.connect(self.helpSetting)
        self.pushButton_setSetting.clicked.connect(self.setSetting)

        # 2.    Video
        # 2.1   Video Player
        self.pushButton_startVideo.clicked.connect(self.startVideo)
        # self.pushButton_stopVideo.clicked.connect(self.stopVideo)
        self.pushButton_showLog.setVisible(False)
        self.pushButton_showLog.clicked.connect(self.showLog)

        # 2.2   Capture
        # self.tableView_Capture()
        self.lcdNumber_ShortVehicle.display("140")
        self.lcdNumber_LongVehicle.display("130")
        self.label_videoFps.setText("fps : {0}/second".format("20"))

        # 3.    Log
        # 3.1   Search
        self.dateEdit_fromDate.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_fromDate.setCalendarPopup(True)

        self.dateEdit_untilDate.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_untilDate.setCalendarPopup(True)

        self.pushButton_searchLog.clicked.connect(self.searchLog)
        self.pushButton_clearLog.clicked.connect(self.clearLog)

        # 3.2   View Log
        # self.tableView_searchLog()
        self.lcdNumber_logShortVehicle.display("20")
        self.lcdNumber_logLongVehicle.display("20")

    # Function Menu Bar
    # Menu File
    def file_exit(self):
        print "good bye bro.."
        sys.exit()

    # Function Tab 1. Setting
    def cekVideoInput(self):
        if self.radioButton_choseFile.setChecked(True):
            print "Chose file"
        elif self.radioButton_choseDevice.setChecked(True):
            print "Device"

    def selectFile(self):
        global fileLoc

        file_filter = "Movie (*.mp4 *.avi *.mkv)"
        filename = QFileDialog.getOpenFileName(self, "Open File", '', file_filter, None,
                                               QFileDialog.DontUseNativeDialog)

        print "file yg di select {0}".format(filename)
        self.label_selectFile.setText(format(filename))

        fileLoc = format(filename)
        return fileLoc

    def selectionDevice(self):
        global fileLoc

        select = self.comboBox_choseDevice.currentText()
        print "Current index selection ", select

        fileLoc = int(select)
        return fileLoc

    def radioChoseFile(self, enabled):
        if enabled:
            self.pushButton_selectFile.setEnabled(True)
        else:
            self.pushButton_selectFile.setEnabled(False)

    def radioChoseDevice(self, enabled):
        if enabled:
            self.comboBox_choseDevice.setEnabled(True)
        else:
            self.comboBox_choseDevice.setEnabled(False)

    def setSetting(self):
        # Get data video mode
        if self.radioButton_rgbVM.isChecked():
            video_mode = "rgb"
        elif self.radioButton_gsVM.isChecked():
            video_mode = "gs"
        elif self.radioButton_hsvVM.isChecked():
            video_mode = "hsv"
        elif self.radioButton_edVM.isChecked():
            video_mode = "edg"

        # Get data video mode
        boundary = self.checkBox_showboundaryVM.isChecked()
        roi = self.checkBox_showroiVM.isChecked()

        # Get data camera from setting
        alt = self.lineEdit_altitudeCam.text()
        elevated = self.lineEdit_elevatedCam.text()
        fps = self.lineEdit_fps.text()

        # Get speed detection method
        if self.radioButton_EuclideanModel.isChecked():
            speed_method = "euclidean"
        elif self.radioButton_PinHoleModel.isChecked():
            speed_method = "pinhole"

        print "Camera Input"
        print "video input: {0}".format(fileLoc)
        print "video mode: {0}".format(video_mode)
        print "boundary: {0}".format(boundary)
        print "roi: {0}".format(roi)
        print "speed detection: {0}".format(speed_method)
        print "alt: {0} | elevated: {1} | fps: {2}".format(alt, elevated, fps)

        time.sleep(1)

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentIndex(1)

    def helpSetting(self):
        title = "Panduan Singkat"
        filename = "conf/help.txt"

        print "Open new popup help"
        self.help_win = HelpInit(title, filename, None)
        self.help_win.show()

    # Function Tab 2. Video
    def startVideo(self):
        fps = 30

        self.tabWidget.setTabEnabled(0, False)

        if not self.capture:
            self.capture = cap_init.QtCapture(fps, fileLoc)
            self.pushButton_pauseVideo.clicked.connect(self.capture.stop)
            self.pushButton_stopVideo.clicked.connect(self.stopVideo)
            # self.capture.setFPS(1)
            self.capture.setParent(self.video_frame)

        self.capture.start()
        self.capture.show()

    def pauseVideo(self):
        self.videoPlayer.pause()

    def stopVideo(self):
        self.capture.deleteLater()
        self.capture = None

        self.tabWidget.setTabEnabled(0, True)
        self.pushButton_showLog.setVisible(True)

    def showLog(self):

        time.sleep(1)

        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(2)

    # Function Tab 3. Log
    def searchLog(self):
        hLabel = ["No", "Date", "Time", "Type", "Speed", "Picture"]
        row = 4
        column = 6

        fromDate = self.dateEdit_untilDate.date().toPyDate()
        untilDate = self.dateEdit_untilDate.date().toPyDate()

        self.tableWidget_searchLog.setRowCount(row)
        self.tableWidget_searchLog.setColumnCount(column)
        self.tableWidget_searchLog.setHorizontalHeaderLabels(hLabel)

        self.tableWidget_searchLog.setItem(0, 0, QTableWidgetItem("Item (0,0)"))
        self.tableWidget_searchLog.setItem(0, 1, QTableWidgetItem("Item (3,0)"))
        self.tableWidget_searchLog.setItem(2, 3, QTableWidgetItem("Item (1,0)"))

        print "mulai dari tanggal {0}".format(fromDate)
        print "hingga tanggal {0}".format(untilDate)

        self.lcdNumber_logShortVehicle.display("50")
        self.lcdNumber_logLongVehicle.display("10")

    def clearLog(self):
        self.tableWidget_searchLog.clear()

    def ujicoba(self):
        print "Open new popup"

