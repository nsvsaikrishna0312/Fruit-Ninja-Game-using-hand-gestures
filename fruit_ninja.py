import cv2
from cvzone.HandTrackingModule import HandDetector
import mouse
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)
frameR = 100

detector = HandDetector(detectionCon=0.65, maxHands=1)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    cv2.rectangle(img, (frameR, frameR), (cam_w - frameR, cam_h - frameR), (255, 0, 255), 2)

    if hands:
        hand = hands[0]
        if 'lmList' in hand:
            lmlist = hand['lmList']
            ind_x, ind_y = lmlist[8][0], lmlist[8][1]
            cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
            conv_x = int(np.interp(ind_x, (0, cam_w), (0, 1536)))
            conv_y = int(np.interp(ind_y, (0, cam_h), (0, 864)))
            mouse.move(conv_x, conv_y)
            fingers = detector.fingersUp(hand)
            if fingers[4] == 1:
                pyautogui.mouseDown()