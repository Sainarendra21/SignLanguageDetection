import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import os, os.path
from keras.models import load_model
import traceback


capture = cv2.VideoCapture(0)

hand_detector_1 = HandDetector(maxHands=1)
hand_detector_2 = HandDetector(maxHands=1)

count = len(os.listdir("D://your_test_data_directory//Gray_imgs//A"))

parent_dir = "A"
child_dir = "a"

offset = 20
step = 1
flag = False
suv = 0
white = np.ones((300, 300), np.uint8) * 255
cv2.imwrite("D:\\Users\\sainarendra\\groupproject\\dev.jpg", white)

while True:
    try:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        hands = hand_detector_1.findHands(frame, draw=False, flipType=True)
        img_final = img_final1 = img_final2 = 0

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            image = frame[y - offset:y + h + offset, x - offset:x + w + offset]

            roi = image  # RGB image without drawing

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (1, 1), 2)

            gray2 = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur2 = cv2.GaussianBlur(gray2, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(blur2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            ret, test_image = cv2.threshold(th3, 27, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            test_image1 = blur
            img_final1 = np.ones((300, 300), np.uint8) * 148
            h = test_image1.shape[0]
            w = test_image1.shape[1]
            img_final1[((300 - h) // 2):((300 - h) // 2) + h, ((300 - w) // 2):((300 - w) // 2) + w] = test_image1

            img_final = np.ones((300, 300), np.uint8) * 255
            h = test_image.shape[0]
            w = test_image.shape[1]
            img_final[((300 - h) // 2):((300 - h) // 2) + h, ((300 - w) // 2):((300 - w) // 2) + w] = test_image

        hands = hand_detector_1.findHands(frame, draw=False, flipType=True)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            image = frame[y - offset:y + h + offset, x - offset:x + w + offset]
            white = cv2.imread("C:\\Users\\your_username\\PycharmProjects\\your_project_name\\white.jpg")
            handz = hand_detector_2.findHands(image, draw=False, flipType=True)
            if handz:
                hand = handz[0]
                pts = hand['lmList']

                os = ((300 - w) // 2) - 10
                os1 = ((300 - h) // 2) - 10
                for t in range(0, 4, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1),
                             (0, 255, 0), 3)
                # ... (rest of the drawing code)

                cv2.imshow("skeleton", white)

            hands = hand_detector_1.findHands(white, draw=False, flipType=True)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                cv2.rectangle(white, (x - offset, y - offset), (x + w, y + h), (3, 255, 25), 3)

            image1 = frame[y - offset:y + h + offset, x - offset:x + w + offset]

            roi1 = image1  # RGB image with drawing

            gray1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray1, (1, 1), 2)

            test_image2 = blur1
            img_final2 = np.ones((300, 300), np.uint8) * 148
            h = test_image2.shape[0]
            w = test_image2.shape[1]
            img_final2[((300 - h) // 2):((300 - h) // 2) + h, ((300 - w) // 2):((300 - w) // 2) + w] = test_image2

            cv2.imshow("binary", img_final)

        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:
            break
        if interrupt & 0xFF == ord('n'):
            parent_dir = chr(ord(parent_dir) + 1)
            child_dir = chr(ord(child_dir) + 1)
            if ord(parent_dir) == ord('Z') + 1:
                parent_dir = "A"
                child_dir = "a"
            flag = False
            count = len(os.listdir("D:\\Users\\sainarendra\\groupproject\\dev.jpg" + parent_dir + "//"))

        if interrupt & 0xFF == ord('a'):
            if flag:
                flag = False
            else:
                suv = 0
                flag = True

        print("=====", flag)
        if flag == True:
            if suv == 50:
                flag = False
            if step % 2 == 0:
                cv2.imwrite("D:\\test_data_2.0\\Gray_imgs\\" + parent_dir + "\\" + child_dir + str(count) + ".jpg",
                            img_final1)
                cv2.imwrite(
                    "D:\\test_data_2.0\\Gray_imgs_with_drawing\\" + parent_dir + "\\" + child_dir + str(count) + ".jpg",
                    img_final2)
                count += 1
                suv += 1
            step += 1
    except Exception:
        print("==", traceback.format_exc())

capture.release()
cv2.destroyAllWindows()
