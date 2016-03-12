import cv2
import numpy as np
import vehicle_tracking as proc
import time

from PyQt4 import QtGui, QtCore
from PyQt4 import uic

main_ui = uic.loadUiType("gtk/video_frame.ui")[0]
start_time = None
width = 960     # pixel
height = 540    # pixel
alpha = 5       # second

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
        global start_time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.fps)
        start_time = time.time()
        print format(start_time)
        return start_time

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()

    def nextFrame(self):
        ret, frame_ori = self.cap.read()

        # ---------- Do not disturb this source code ---------- #
        # Default color model is BGR format
        frame_ori = proc.resize(frame_ori, width, height)       # resize video frame for fits within the frame
        rgb_frame = proc.convBGR2RGB(frame_ori)                 # convert from BGR color model to RGB color model
        # ----------------------------------------------------- #

        # Function for operation the feature
        gray_frame = proc.convRGB2GRAY(rgb_frame)               # convert from RGB to Gray scale

        # Get background subtraction from moving object
        real_time = time.time()
        if real_time > start_time + alpha:
            print "sudah lebih waktunya"
        else:
            print real_time

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
        proc.addText(gray_frame, "kesatu", 100, 300)

        # Last variable to show must 'show_frame'
        show_frame = gray_frame

        # ---------- Do not disturb this source code ----------- #
        # Gray scale, binary image - Format_Indexed8
        # RGB image - Format_RGB888
        img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        # ------------------------------------------------------ #
