import numpy as np
import cv2
import os
import pyttsx3
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
import enchant
import tkinter as tk
from PIL import Image, ImageTk

english_dict = enchant.Dict("en-US")

hand_detector_main = HandDetector(maxHands=1)
hand_detector_secondary = HandDetector(maxHands=1)
hand_offset = 29

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

class SignLanguageApp:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_image = None
        self.sign_language_model = load_model('/cnn8grps_rad1_model.h5')
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty("rate", 100)
        self.speech_engine.setProperty("voice", self.speech_engine.getProperty("voices")[0].id)
        self.character_count = {'blank': 0, **{char: 0 for char in ascii_uppercase}}
        self.blank_flag, self.space_flag, self.next_flag, self.prev_char, self.frame_count = 0, False, True, "", -1
        self.ten_prev_chars = [" "] * 10
        self.initialize_ui()

        print("Loaded model from disk")

        self.root.mainloop()

    def initialize_ui(self):
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1300x700")
        self.image_panel, self.image_panel_2 = self.create_image_panel(100), self.create_image_panel(600)
        self.text_panel, self.button_1, self.button_2, self.button_3 = self.create_text_button_widgets(500, 500, 550, 600, 650)

    def create_image_panel(self, x):
        image_panel = tk.Label(self.root)
        image_panel.place(x=x, y=3, width=480, height=640)
        return image_panel

    def create_text_button_widgets(self, x, *y_values):
        widgets = [
            tk.Label(self.root, text="", font=("Courier", 30)),
            *[tk.Button(self.root, text="", font=("Courier", 20), wraplength=825) for _ in range(3)]
        ]
        for widget, y in zip(widgets, [x, *y_values]):
            widget.place(x=500, y=y)
        return widgets

    def video_loop(self):
        try:
            ok, frame = self.video_capture.read()
            cv2_image = cv2.flip(frame, 1)
            hands = hand_detector_main.findHands(cv2_image, draw=False, flipType=True)
            cv2_image_copy = np.array(cv2_image)
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2_image)
            img_tk = ImageTk.PhotoImage(image=self.current_image)
            self.image_panel.img_tk, self.image_panel.config(image=img_tk)

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                hand_image = cv2_image_copy[y - hand_offset:y + h + hand_offset, x - hand_offset:x + w + hand_offset]

                white_background = cv2.imread("D:\\Users\\sainarendra\\groupproject\\dev.jpg")

                detected_hands = hand_detector_secondary.findHands(hand_image, draw=False, flipType=True)
                self.frame_count += 1
                if detected_hands:
                    hand = detected_hands[0]
                    hand_points = hand['lmList']
                    offset_x, offset_y = ((400 - w) // 2) - 15, ((400 - h) // 2) - 15

                    for t in range(0, 4, 1):
                        cv2.line(white_background, (hand_points[t][0] + offset_x, hand_points[t][1] + offset_y),
                                 (hand_points[t + 1][0] + offset_x, hand_points[t + 1][1] + offset_y), (0, 255, 0), 3)

                    cv2.line(white_background, (hand_points[0][0] + offset_x, hand_points[0][1] + offset_y),
                             (hand_points[17][0] + offset_x, hand_points[17][1] + offset_y), (0, 255, 0), 3)

                    for i in range(21):
                        cv2.circle(white_background, (hand_points[i][0] + offset_x, hand_points[i][1] + offset_y), 2,
                                   (0, 0, 255), 1)

                    result_image = white_background
                    self.predict(result_image)

                    self.current_image_2 = Image.fromarray(result_image)

                    img_tk = ImageTk.PhotoImage(image=self.current_image_2)

                    self.image_panel_2.img_tk, self.image_panel_2.config(image=img_tk)

                    self.text_panel.config(text=self.current_symbol, font=("Courier", 30))
                    buttons_info = zip([self.button_1, self.button_2, self.button_3], [self.word_1, self.word_2, self.word_3])

                    for button, word in buttons_info:
                        button.config(text=word, font=("Courier", 20), wraplength=825)

            self.root.after(10, self.video_loop)

        except Exception as e:
            print(f"Exception: {e}\n{traceback.format_exc()}")

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.video_capture.release()


if __name__ == "__main__":
    app = SignLanguageApp()
