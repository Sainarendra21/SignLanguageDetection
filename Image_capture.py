import os
import cv2
import uuid

IMAGE_PATH = "CollectedImages"
labels = ["Hi", "Fine", "Not Ok", "Thanks", "Sorry", "Namasthe", "Please", "I Love You", "How are you", "Nice", "Excuse Me"]
num_of_img = 15

for label in labels:
    img_path = os.path.join(IMAGE_PATH, label)
    os.makedirs(img_path, exist_ok=True)
    print('Capturing images for {}'.format(label))
    input("Press Enter to start capturing images...")
    
    for imagenumber in range(1, num_of_img + 1):
        cap = cv2.VideoCapture(0)
        
        ret, frame = cap.read()
        imagename = os.path.join(img_path, '{}_{}.jpg'.format(label, imagenumber))
        cv2.imwrite(imagename, frame)
        print('Image {} captured'.format(imagenumber))
        cap.release()
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print("Image capture completed for all labels.")
