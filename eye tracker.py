import cv2
import mediapipe as mp
import pyautogui as pg
def main():
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

            #considering a few limited landmarks to track them down
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
            

            #first 2 for left eye next for right eye
            eye_landmarks = [landmarks[472], landmarks[159],landmarks[477],landmarks[386]]
            
            #highlighting eyelid landmarks
            for landmark in eye_landmarks:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
            #detecting left eye blink to click
            print(eye_landmarks[0].y - eye_landmarks[1].y,eye_landmarks[2].y - eye_landmarks[3].y)

            #avoinding while natural blinking
            if((eye_landmarks[0].y - eye_landmarks[1].y) < 0.019) and ((eye_landmarks[3].y - eye_landmarks[2].y) < 0.019):
                continue
            #if coord 71.y > 21.y -> scroll up
            if (landmark[71].y > landmark[21].y):
                pg.scroll(100)
            #if coord 71.y < 162.y -> scroll down
            if (landmark[71].y < landmark[162].y):
                pg.scroll(-100)
            #left click
            if (eye_landmarks[0].y - eye_landmarks[1].y) < 0.017:
                pg.click()
            #right click
            if (eye_landmarks[2].y - eye_landmarks[3].y) < 0.017:
                pg.click(button="right")
        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)
        # Press 'Esc' to exit
        if cv2.waitKey(1) & 0xFF == 27:  
            break
    cam.release()
    cv2.destroyAllWindows()

main()
    
