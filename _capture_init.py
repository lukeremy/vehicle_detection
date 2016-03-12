import cv2
import numpy as np
import vehicle_tracking as vtrack

from PyQt4 import QtGui, QtCore
from PyQt4 import uic

main_ui = uic.loadUiType("gtk/video_frame.ui")[0]
width = 960
height = 540


class QtCapture(QtGui.QFrame, main_ui):
    def __init__(self, fps, filename):
        super(QtGui.QFrame, self).__init__()

        self.fps = fps
        self.setupUi(self)
        # file = "assets/binaryImg.jpg"

        # Start Capture Video
        self.cap = cv2.VideoCapture(filename)

    def setFPS(self, fps):
        self.fps = fps

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()

    def nextFrame(self):
        ret, frame_ori = self.cap.read()

        # ---------- Do not disturb this source code ---------- #
        # Default color model is BGR format
        frame_ori = cv2.resize(frame_ori, (width, height))      # resize video frame for fits within the frame
        rgb_frame = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2RGB)  # convert from BGR color model to RGB color model
        # ----------------------------------------------------- #

        # Function for operation the feature
        gray_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2GRAY)
        # bin_frame = cv2.threshold(gray_frame, 20, 255, cv2.THRESH_BINARY)
        # ret, thresh = cv2.threshold(gray_frame, 127, 255, 0)
        # Edge Detection
        # Binary image in edge detection is get from gray scale feature
        # edge_frame = cv2.Canny(gray_frame, 100, 200)

        # Morphology Operation
        # kernel = np.ones((2, 2), np.uint8)
        # erosi = cv2.dilate(edge_frame, kernel, iterations=1)

        # Add rectangle for every vehicle
        # 9cv2.rectangle(gray_frame, (200, 300), (500, 500), (0, 255, 255), 2, 0, 0)

        # Add Text
        #font = cv2.FONT_HERSHEY_PLAIN
        #gambar = "budiman"
        #cv2.putText(gray_frame, "{0}".format(gambar), (100, 300), font, 0.9, (255, 255, 0), 1)

        vtrack.addText(gray_frame, "kesatu", 100, 300)

        # Last variable to show must 'show_frame'
        show_frame = gray_frame

        # ---------- Do not disturb this source code ----------- #
        # Gray scale, binary image - Format_Indexed8
        # RGB image - Format_RGB888
        img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        # ------------------------------------------------------ #


