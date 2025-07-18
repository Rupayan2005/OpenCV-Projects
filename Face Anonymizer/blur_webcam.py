import cv2
import mediapipe as mp
import argparse

def process_image(img,face_detection):
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

            # img = cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,255,0),5) #just create a rectangular box around the face
            # Blur Faces
            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w, :], (30, 30))

    return img

args = argparse.ArgumentParser()
args.add_argument("--mode", default='webcam')
args.add_argument("--filepath", default=None)

args = args.parse_args()


#Detect Faces
mp_face_detection = mp.solutions.face_detection
with mp_face_detection.FaceDetection(model_selection=0,min_detection_confidence=0.5) as face_detection:
    if args.mode in ['webcam']:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        while ret:
            frame = process_image(frame,face_detection)
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            ret,frame = cap.read()
        cap.release()