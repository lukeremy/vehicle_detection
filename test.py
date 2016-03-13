# Main Library
import cv2
import numpy as np
import os
import pygame

# Additional Library
#import mainInterface
# from ui_imagedialog import Ui_ImageDialog

# os.chdir("/")
# vid_file_ori = "/home/auzan/PycharmProjects/VehicleCounting/assets/IP Camera Highway Surveillance.mp4"

vid_file_ori = "assets/IP Camera Highway Surveillance.mp4"
iteration = 1
cap = cv2.VideoCapture(vid_file_ori)
height = 960
width = 540

while True:
    # Capture frame by frame
    ret, frame_ori = cap.read()
    iteration += 1

    if iteration == 30:
        iteration = 1

    # FrameRate
    fps = cap.get(cv2.CAP_PROP_FPS)
    print "Frame per second {0}".format(fps)

    # Operation on the frameq
    assert isinstance(frame_ori, object)
    #frame_ori = cv2.resize(frame_ori, (height, width), interpolation = cv2.INTER_CUBIC)
    gray_frame = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2GRAY)
    hsv_frame = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2HSV)
    h_fhsv, s_fhsv, v_fhsv = cv2.split(hsv_frame)

    # Edge detection
    edge_frame = cv2.Canny(gray_frame, 100, 200)

    # Morphology Operation
    kernel = np.ones((2, 2), np.uint8)
    erosi = cv2.dilate(edge_frame, kernel, iterations=1)

    # Add rectangle for every vehicle
    cv2.rectangle(frame_ori, (200 + iteration, 300 + iteration), (500, 500), (0, 255, 255), 2, 0, 0)

    # Add Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    gambar = "budiman"
    cv2.putText(frame_ori, "{0}".format(gambar), (100, 300), font, 0.9, (255, 255, 0), 2)

    # Display the result
    cv2.imshow('grayscale frame', edge_frame)
    print "iteration {0}", format(iteration)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()