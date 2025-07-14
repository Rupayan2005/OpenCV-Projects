import cv2
import mediapipe as mp

# Initialize FaceMesh globally for efficiency
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True,
                                  max_num_faces=1,
                                  min_detection_confidence=0.5)

def get_face_landmarks(image, draw=False):
    """
    Accepts a grayscale or BGR image, returns 1404 normalized face mesh landmarks.
    """
    if image is None:
        return []  # Image could not be read

    # Check and convert grayscale to RGB
    if len(image.shape) == 2:  # Grayscale
        image_input_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 3:  # BGR
        image_input_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        return []  # Unsupported image format

    results = face_mesh.process(image_input_rgb)

    image_landmarks = []

    if results.multi_face_landmarks:
        ls_single_face = results.multi_face_landmarks[0].landmark
        xs_ = [l.x for l in ls_single_face]
        ys_ = [l.y for l in ls_single_face]
        zs_ = [l.z for l in ls_single_face]

        for j in range(len(xs_)):
            image_landmarks.append(xs_[j] - min(xs_))
            image_landmarks.append(ys_[j] - min(ys_))
            image_landmarks.append(zs_[j] - min(zs_))

    return image_landmarks
