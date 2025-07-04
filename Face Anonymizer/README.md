# Face Anonymizer Project

A web-based application that automatically detects and blurs faces in images and videos to protect privacy and anonymize individuals. Built with OpenCV for computer vision processing, Streamlit for the frontend interface, and a Python backend for handling the core anonymization logic.

## Features

- **Image Face Anonymization**: Upload images and automatically blur detected faces
- **Video Face Anonymization**: Process video files with real-time face detection and blurring
- **Interactive Web Interface**: User-friendly Streamlit frontend for easy file uploads
- **Customizable Blur Intensity**: Adjustable blur strength with slider control (0-1 range)
- **Download Processed Files**: Download anonymized images and videos directly
- **Real-time Processing**: Efficient face detection using OpenCV
- **Multiple Format Support**: Supports common image formats (JPG, PNG, JPEG) and video formats (MP4)

## Project Structure

```
face-anonymizer/
├── frontend.py                   # Streamlit frontend application
├── blur_backend.py               # Core anonymization logic
├── blur_image.py                 # simple anonymization logic testing file for Images/Videos
├── blur_webcam.py                # Anonymization logic for Webcam
├── data/                         # Temporary upload directory
├── output/                       # Processed files directory
├── README.md                     # Project documentation
└── requirements.txt              # Main project dependencies
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Git (optional, for cloning)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rupayan2005/OpenCV-Projects.git
   cd Face Anonymizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir data output
   ```

## Usage

### Running the Application

1. **Start the Streamlit frontend**
   ```bash
   streamlit run frontend.py
   ```

2. **Access the application**
   Open your web browser and navigate to `http://localhost:8501`

### Using the Interface

1. **Upload Files**: Choose between image or video upload options
2. **Select File**: Click "Browse files" to select your image or video
3. **Adjust Blur Intensity**: Use the slider to set blur strength (0.0 = no blur, 1.0 =maximum blur)
4. **Process**: The application will automatically detect and blur faces
5. **Preview**: View the processed result in the interface
6. **Download**: Click the download button to save the anonymized file

### Supported File Formats

**Images:**
- JPEG (.jpg, .jpeg)
- PNG (.png)

**Videos:**
- MP4 (.mp4)

## Configuration

### Blur Settings

You can adjust the blur intensity directly in the Streamlit interface using the slider control:

```python
# Blur intensity range (0 to 100)
# 0 = No blur (original image)
# 100 = Maximum blur (completely anonymized)
BLUR_INTENSITY_RANGE = (0, 100)

# Default blur intensity
DEFAULT_BLUR_INTENSITY = 30

# Face detection confidence threshold
CONFIDENCE_THRESHOLD = 0.5
```

## Dependencies

### Main Dependencies
- **OpenCV**: Computer vision and image processing
- **Streamlit**: Web application framework
- **NumPy**: Numerical computing
- **Pillow**: Image processing
- **Mediapipe**: Face detection

### Full Requirements
```
opencv-python>=4.5.0
streamlit>=1.28.0
mediapipe>=0.10.0
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Privacy and Ethics

This tool is designed to protect privacy by anonymizing faces in media files. Please use responsibly and ensure you have proper consent when processing media containing other individuals.

## Acknowledgments

- OpenCV community for computer vision tools
- Streamlit team for the excellent web framework

## Contact

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.

---
