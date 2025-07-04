import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from blur_backend import FaceBlurProcessor

# Configure page
st.set_page_config(
    page_title="Face Blur App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .feature-box {
        background: #000;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }

    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }

    .success-box {
        background: #000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }

    .info-box {
        background: #000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .sidebar .stSlider {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .metric-container {
        background: #000;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'processed_video_path' not in st.session_state:
    st.session_state.processed_video_path = None
if 'face_count' not in st.session_state:
    st.session_state.face_count = 0


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎭 Face Blur Application</h1>
        <p>Privacy-focused face blurring for images and videos using AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # Blur intensity slider
        blur_intensity = st.slider(
            "Blur Intensity",
            min_value=10,
            max_value=100,
            value=30,
            step=5,
            help="Higher values create more blur"
        )

        # Detection confidence slider
        detection_confidence = st.slider(
            "Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Higher values require more confident face detection"
        )

        # Model selection
        model_selection = st.selectbox(
            "Detection Model",
            [0, 1],
            index=0,
            help="0: Within 2 meters, 1: Within 5 meters"
        )

        st.markdown("---")
        st.markdown("### 📊 Processing Stats")

        # Display stats
        if st.session_state.face_count > 0:
            st.markdown(f"""
            <div class="metric-container">
                <h3>👥 Faces Detected</h3>
                <h2 style="color: #667eea;">{st.session_state.face_count}</h2>
            </div>
            """, unsafe_allow_html=True)

    # Features section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🖼️ Image Processing</h3>
            <p>Upload and blur faces in images instantly with customizable settings</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🎥 Video Processing</h3>
            <p>Process videos frame by frame with real-time progress tracking</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>🔒 Privacy First</h3>
            <p>All processing happens locally on your device. No data uploaded to servers</p>
        </div>
        """, unsafe_allow_html=True)

    # File upload section
    st.markdown("## 📁 Upload Your File")

    # Mode selection
    mode = st.selectbox(
        "Choose processing mode:",
        ["Image", "Video"],
        help="Select whether you want to process an image or video file"
    )

    # File uploader
    if mode == "Image":
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Supported formats: JPG, JPEG, PNG, BMP"
        )
    else:
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Supported formats: MP4, AVI, MOV, MKV"
        )

    if uploaded_file is not None:
        # Display file info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.markdown(f"""
        <div class="info-box">
            📄 <strong>File:</strong> {uploaded_file.name}<br>
            📏 <strong>Size:</strong> {file_size_mb:.2f} MB
        </div>
        """, unsafe_allow_html=True)

        # Initialize processor with current settings
        processor = FaceBlurProcessor(
            model_selection=model_selection,
            min_detection_confidence=detection_confidence,
            blur_intensity=blur_intensity
        )

        # Processing section
        st.markdown("## 🔄 Processing")

        if mode == "Image":
            # Display original image
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Original Image")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)

            # Process button
            if st.button("🎯 Blur Faces", key="process_image"):
                with st.spinner("Processing image..."):
                    # Convert PIL to OpenCV
                    img_array = np.array(image)
                    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                    # Count faces first
                    face_count = processor.count_faces(img_cv)
                    st.session_state.face_count = face_count

                    # Process image
                    processed_img = processor.process_image(img_cv)

                    # Save to output directory (like original code)
                    output_dir = "./output"
                    os.makedirs(output_dir, exist_ok=True)
                    name, ext = os.path.splitext(uploaded_file.name)
                    output_path = os.path.join(output_dir, f"{name}_o{ext}")
                    cv2.imwrite(output_path, processed_img)

                    # Convert back to RGB for display
                    processed_img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                    processed_pil = Image.fromarray(processed_img_rgb)

                    # Store in session state
                    st.session_state.processed_image = processed_pil
                    st.session_state.processed_cv_image = processed_img
                    st.session_state.saved_image_path = output_path

                st.markdown(f"""
                <div class="success-box">
                    ✅ <strong>Image processed successfully!</strong><br>
                    👥 Detected and blurred {st.session_state.face_count} face(s)<br>
                    💾 Saved to: <code>{output_path}</code>
                </div>
                """, unsafe_allow_html=True)

                # Rerun to update sidebar stats
                st.rerun()

            # Display processed image
            if 'processed_image' in st.session_state and st.session_state.processed_image is not None:
                with col2:
                    st.markdown("### Processed Image")
                    st.image(st.session_state.processed_image, use_container_width=True)

                    # Display saved file path
                    if 'saved_image_path' in st.session_state:
                        st.info(f"💾 **Saved to:** `{st.session_state.saved_image_path}`")

                    # Download button (additional option)
                    img_bytes = cv2.imencode('.jpg', st.session_state.processed_cv_image)[1].tobytes()
                    st.download_button(
                        label="📥 Download Blurred Image",
                        data=img_bytes,
                        file_name=f"blurred_{uploaded_file.name}",
                        mime="image/jpeg",
                        use_container_width=True,
                        help="Alternative: File is already saved in ./output/ directory"
                    )

        else:  # Video processing
            st.markdown("### Video Processing")

            # Save uploaded video temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_video_path = tmp_file.name

            # Display video info
            cap = cv2.VideoCapture(temp_video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()

            st.markdown(f"""
            <div class="info-box">
                🎬 <strong>Duration:</strong> {duration:.1f}s<br>
                📺 <strong>Resolution:</strong> {width}x{height}<br>
                🎞️ <strong>FPS:</strong> {fps}<br>
                📋 <strong>Total Frames:</strong> {frame_count}
            </div>
            """, unsafe_allow_html=True)

            # Process button
            if st.button("🎯 Blur Faces in Video", key="process_video"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                def progress_callback(progress):
                    progress_bar.progress(progress)
                    status_text.text(f"Processing... {progress * 100:.1f}%")

                with st.spinner("Processing video... This may take a while depending on video length."):
                    try:
                        # Create output directory and path (like original code)
                        output_dir = "./output"
                        os.makedirs(output_dir, exist_ok=True)
                        name, ext = os.path.splitext(uploaded_file.name)
                        output_path = os.path.join(output_dir, f"{name}_o{ext}")

                        # Process video with specific output path
                        final_output_path = processor.process_video(
                            temp_video_path,
                            output_path=output_path,
                            progress_callback=progress_callback
                        )

                        st.session_state.processed_video_path = final_output_path
                        st.session_state.saved_video_path = final_output_path

                        st.markdown(f"""
                        <div class="success-box">
                            ✅ <strong>Video processed successfully!</strong><br>
                            🎥 All faces in the video have been blurred<br>
                            💾 Saved to: <code>{final_output_path}</code>
                        </div>
                        """, unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Error processing video: {str(e)}")
                    finally:
                        progress_bar.empty()
                        status_text.empty()

            # Download processed video
            if 'processed_video_path' in st.session_state and st.session_state.processed_video_path:
                try:
                    # Display saved file path
                    if 'saved_video_path' in st.session_state:
                        st.info(f"💾 **Saved to:** `{st.session_state.saved_video_path}`")

                    with open(st.session_state.processed_video_path, 'rb') as file:
                        video_bytes = file.read()
                        st.download_button(
                            label="📥 Download Blurred Video",
                            data=video_bytes,
                            file_name=f"blurred_{uploaded_file.name}",
                            mime="video/mp4",
                            use_container_width=True,
                            help="Alternative: File is already saved in ./output/ directory"
                        )
                except Exception as e:
                    st.error(f"Error reading processed video: {str(e)}")

            # Clean up temp file
            try:
                if os.path.exists(temp_video_path):
                    os.unlink(temp_video_path)
            except:
                pass

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🔒 <strong>Privacy Notice:</strong> All processing happens locally on your device. No data is sent to external servers.</p>
        <p>🚀 Made with ❤️ using Streamlit, OpenCV, and MediaPipe</p>
        <p>⚡ Powered by Google's MediaPipe for accurate face detection</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()