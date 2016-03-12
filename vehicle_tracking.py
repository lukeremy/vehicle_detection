import cv2


def addText(frame, text, x, y):
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame, "{0}".format(text), (x, y), font, 0.9, (255, 255, 0), 1)