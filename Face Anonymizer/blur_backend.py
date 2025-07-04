import cv2
import mediapipe as mp
import argparse
import tempfile
import os
import numpy as np


class FaceBlurProcessor:
    """Core face blurring processor using MediaPipe"""

    def __init__(self, model_selection=0, min_detection_confidence=0.5, blur_intensity=30):
        self.model_selection = model_selection
        self.min_detection_confidence = min_detection_confidence
        self.blur_intensity = blur_intensity
        self.mp_face_detection = mp.solutions.face_detection

    def process_image(self, img):
        """Process image to blur detected faces"""
        with self.mp_face_detection.FaceDetection(
                model_selection=self.model_selection,
                min_detection_confidence=self.min_detection_confidence
        ) as face_detection:

            H, W, _ = img.shape
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces = face_detection.process(img_rgb)

            if faces.detections is not None:
                for detection in faces.detections:
                    location_data = detection.location_data
                    bbox = location_data.relative_bounding_box

                    x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                    x1 = int(x1 * W)
                    y1 = int(y1 * H)
                    w = int(w * W)
                    h = int(h * H)

                    # Blur the face region
                    img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(
                        img[y1:y1 + h, x1:x1 + w, :],
                        (self.blur_intensity, self.blur_intensity)
                    )

            return img

    def process_uploaded_file(self, uploaded_file, file_type='image'):
        """Process uploaded file from Streamlit"""
        if file_type == 'image':
            return self._process_uploaded_image(uploaded_file)
        elif file_type == 'video':
            return self._process_uploaded_video(uploaded_file)

    def _process_uploaded_image(self, uploaded_file):
        """Process uploaded image file"""
        # Convert uploaded file to numpy array
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode the uploaded image")

        # Count faces before processing
        face_count = self.count_faces(img)

        # Process image
        processed_img = self.process_image(img.copy())

        return processed_img, face_count

    def _process_uploaded_video(self, uploaded_file):
        """Process uploaded video file"""
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_input_path = tmp_file.name

        # Create temporary output file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_output:
            temp_output_path = tmp_output.name

        try:
            # Process video
            self.process_video(temp_input_path, temp_output_path)

            # Read processed video
            with open(temp_output_path, 'rb') as f:
                processed_video_bytes = f.read()

            return processed_video_bytes

        finally:
            # Clean up temporary files
            try:
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
            except:
                pass

    def process_video(self, video_path, output_path=None, progress_callback=None):
        """Process video to blur faces in all frames"""
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create output path if not provided
        if output_path is None:
            dirname, filename = os.path.split(video_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_o{ext}"
            output_path = os.path.join(dirname or ".", output_filename)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        with self.mp_face_detection.FaceDetection(
                model_selection=self.model_selection,
                min_detection_confidence=self.min_detection_confidence
        ) as face_detection:

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Process frame
                processed_frame = self._process_frame(frame, face_detection)
                out.write(processed_frame)

                frame_count += 1

                # Call progress callback if provided
                if progress_callback:
                    progress_callback(frame_count / total_frames)

        cap.release()
        out.release()

        return output_path

    def _process_frame(self, frame, face_detection):
        """Process a single frame for face blurring"""
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_detection.process(frame_rgb)

        if faces.detections is not None:
            for detection in faces.detections:
                location_data = detection.location_data
                bbox = location_data.relative_bounding_box

                x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                x1 = int(x1 * W)
                y1 = int(y1 * H)
                w = int(w * W)
                h = int(h * H)

                # Blur the face region
                frame[y1:y1 + h, x1:x1 + w, :] = cv2.blur(
                    frame[y1:y1 + h, x1:x1 + w, :],
                    (self.blur_intensity, self.blur_intensity)
                )

        return frame

    def process_image_and_save(self, img, input_path):
        """Process image and save to output path derived from input filename"""
        # Generate output path by appending "_o" before the extension
        dirname, filename = os.path.split(input_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_o{ext}"
        output_path = os.path.join(dirname or ".", output_filename)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Process image
        processed_img = self.process_image(img)

        # Save to file
        cv2.imwrite(output_path, processed_img)

        return processed_img, output_path

    def count_faces(self, img):
        """Count number of faces detected in image"""
        with self.mp_face_detection.FaceDetection(
                model_selection=self.model_selection,
                min_detection_confidence=self.min_detection_confidence
        ) as face_detection:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces = face_detection.process(img_rgb)

            if faces.detections is not None:
                return len(faces.detections)
            return 0


def main():
    """Command line interface for face blurring"""
    parser = argparse.ArgumentParser(description='Face Blur Application')
    parser.add_argument("--mode", default='image', choices=['image', 'video'],
                        help='Processing mode: image or video')
    parser.add_argument("--filepath", default=None,
                        help='Path to input file')
    parser.add_argument("--output", default=None,
                        help='Output file path (optional)')
    parser.add_argument("--blur-intensity", type=int, default=30,
                        help='Blur intensity (default: 30)')
    parser.add_argument("--confidence", type=float, default=0.5,
                        help='Minimum detection confidence (default: 0.5)')

    args = parser.parse_args()

    # Check if filepath is provided
    if args.filepath is None:
        print("Error: Please provide a filepath using --filepath argument")
        print("Example: python script.py --filepath /path/to/your/image.jpg")
        return

    # Initialize processor
    processor = FaceBlurProcessor(
        blur_intensity=args.blur_intensity,
        min_detection_confidence=args.confidence
    )

    if args.mode == 'image':
        # Process image
        print(f"Processing image: {args.filepath}")
        img = cv2.imread(args.filepath)

        if img is None:
            print(f"Error: Could not load image from {args.filepath}")
            return

        # Count faces before processing
        face_count = processor.count_faces(img)
        print(f"Detected {face_count} face(s)")

        # Process image
        processed_img = processor.process_image(img)

        # Save result
        _, output_path = processor.process_image_and_save(img, args.filepath)
        print(f"Blurred image saved to: {output_path}")

    elif args.mode == 'video':
        # Process video
        print(f"Processing video: {args.filepath}")

        def progress_callback(progress):
            print(f"Progress: {progress * 100:.1f}%")

        result_path = processor.process_video(
            args.filepath,
            None,  # Let method auto-generate based on input
            progress_callback
        )
        print(f"Blurred video saved to: {result_path}")


if __name__ == "__main__":
    main()