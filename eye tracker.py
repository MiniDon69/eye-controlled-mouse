import cv2
import mediapipe as mp
import pyautogui as pg

#created objects
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pg.size()
#loop used to constantly keep taking frames
while True:
    #reading camera frames
    _, frame = cam.read()

    #fliping the frame and 1 for fliping vertically
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #creating face mech(all the points on face)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        #considering a few limited land marks to track them down
        #there are total 478 landmarks on your face


        #168 needs to be the position for the mouse pointer
        landmark = landmarks[168]
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)

        #for showing the mouse pointer landmark
        #cv2.circle(frame, (x, y), 3, (0, 0, 255))
        screen_x = screen_w * landmark.x
        screen_y = screen_h * landmark.y
        pg.moveTo(screen_x, screen_y)
        #highlighting eyelid landmarks
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
        #detecting left eye blink to click
        if (left[0].y - left[1].y) < 0.04:
            pg.click()
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
