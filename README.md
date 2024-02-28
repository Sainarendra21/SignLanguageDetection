# Sign Language Detection using YOLOv5s

This project focuses on the detection of sign language gestures using YOLOv5s, a state-of-the-art deep learning model for object detection. The model is trained on a custom dataset containing sign language gestures.

## Overview

Sign language detection is crucial for creating inclusive technology that can aid communication for people with hearing impairments. This project aims to develop a robust sign language detection system using computer vision techniques.

## Dataset

The dataset used in this project consists of images of various sign language gestures captured using OpenCV. Each image is labeled using the LabelImg library to provide bounding box annotations for training the YOLOv5s model.

## Training

The YOLOv5s model is trained using the custom dataset for 300 epochs. During training, the model learns to detect different sign language gestures represented in the dataset.

## Results

After training for 300 epochs, the model achieves satisfactory results in detecting sign language gestures. The accuracy and performance metrics are evaluated to assess the effectiveness of the model.

## Requirements

- Python 3.x
- PyTorch
- OpenCV
- LabelImg
- YOLOv5s

## Usage

To use the sign language detection model:

1. Clone this repository:
    ```bash
    git clone https://github.com/Sainarendra21/SignLanguageDetection.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run inference:
    ```bash
    python run.py
    ```

## Future Work

- Improve model performance by collecting more diverse data and fine-tuning the model architecture.
- Deploy the sign language detection model as a web or mobile application for real-time usage.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

