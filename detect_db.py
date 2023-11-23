import numpy as np
import cv2
import os
import sys
import traceback
import pyttsx3
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
import enchant
import tkinter as tk
from PIL import Image, ImageTk

d = enchant.Dict("en-US")
hand_detector1 = HandDetector(maxHands=1)
hand_detector2 = HandDetector(maxHands=1)


offset = 29

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

class SignLanguageApp:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_image = None
        self.model = load_model('/cnn8grps_rad1_model.h5')
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty("rate", 100)
        voices = self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice", voices[0].id)

        self.character_count = {}
        self.character_count['blank'] = 0
        self.blank_flag = 0
        self.space_flag = False
        self.next_flag = True
        self.prev_char = ""
        self.count = -1
        self.ten_prev_char = [" "] * 10

        for char in ascii_uppercase:
            self.character_count[char] = 0

        print("Loaded model from disk")

        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1300x700")

        self.panel = tk.Label(self.root)
        self.panel.place(x=100, y=3, width=480, height=640)

       

        self.video_loop()

    def video_loop(self):
        try:
            ok, frame = self.video_capture.read()
            cv2image = cv2.flip(frame, 1)
            hands = hand_detector1.findHands(cv2image, draw=False, flipType=True)
            cv2image_copy = np.array(cv2image)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]

                white = cv2.imread("d:\\user\\sainarendra\\groupproject\\image.jpg")

                handz = hand_detector2.findHands(image, draw=False, flipType=True)
                print(" ", self.count)
                self.count += 1
                if handz:
                    hand = handz[0]
                    points = hand['lmList']
                    os = ((400 - w) // 2) - 15
                    os1 = ((400 - h) // 2) - 15

                    for t in range(0, 4, 1):
                        cv2.line(white, (points[t][0] + os, points[t][1] + os1), (points[t + 1][0] + os, points[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    
                 

                    cv2.line(white, (points[0][0] + os, points[0][1] + os1), (points[17][0] + os, points[17][1] + os1),
                             (0, 255, 0), 3)

                    for i in range(21):
                        cv2.circle(white, (points[i][0] + os, points[i][1] + os1), 2, (0, 0, 255), 1)

                    result_image = white
                    self.predict(result_image)

                    self.current_image2 = Image.fromarray(result_image)

                    imgtk = ImageTk.PhotoImage(image=self.current_image2)

                    self.panel2.imgtk = imgtk
                    self.panel2.config(image=imgtk)

                    self.panel3.config(text=self.current_symbol, font=("Courier", 30))

                    self.b1.config(text=self.word1, font=("Courier", 20), wraplength=825, command=self.action1)
                    self.b2.config(text=self.word2, font=("Courier", 20), wraplength=825, command=self.action2)
                    self.b3.config(text=self.word3, font=("Courier", 20), wraplength=825, command=self.action3)

            self.root.after(10, self.video_loop)

        except Exception as e:
            print(f"Exception: {e}\n{traceback.format_exc()}")

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.video_capture.release()
if __name__ == "__main__":
    app = SignLanguageApp()
    app.root.mainloop()
