from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])


    C = dist.euclidean(eye[0], eye[3])


    ear = (A + B) / (2.0 * C)


    return ear



EAR_Threshold = 0.3
Frames_Threshold = 10


Frame_Count = 0


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


cap = cv2.VideoCapture(0)
time.sleep(1.0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Looping over frames from the webcam video
while True:

    ret,frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    rects = detector(gray, 0)


    for rect in rects:

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)


        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        EAR = (leftEAR + rightEAR) / 2.0


        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)


        if EAR < EAR_Threshold:
            Frame_Count += 1

            if Frame_Count > Frames_Threshold:
                cv2.putText(frame, "Woah..! Open your Eyes!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        else:
            Frame_Count = 0



    # Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
cap.release()