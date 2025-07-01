# Yellow Object Detection

Real-time yellow object detection using OpenCV and HSV color space filtering.

## Description

This project detects and tracks yellow objects in real-time using webcam input. It utilizes HSV color space conversion and contour detection to identify yellow objects and draw bounding boxes around them.

## Files

- `main.py` - Main application with camera capture and detection logic
- `util.py` - Utility functions and yellow color range definitions
- `requirements.txt` - Project dependencies

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python main.py
```

- Press 'q' to quit the application
- Adjust lighting conditions for better detection accuracy

## Features

- Real-time yellow object detection
- Bounding box visualization
- HSV color space filtering
- Contour-based object identification

## Requirements

- Python 3.7+
- Webcam or camera device
- Good lighting conditions for optimal detection
