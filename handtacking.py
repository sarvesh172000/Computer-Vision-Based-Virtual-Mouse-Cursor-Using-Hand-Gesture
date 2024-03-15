import cv2
import mediapipe
import time
import math
class HandTracker():   

    def __init__(self, image_mode=False, num_hands=1, detec_confi=0.4, track_confi=0.4):

        self.image_mode = image_mode
        self.num_hands = num_hands
        self.detec_confi = detec_confi
        self.track_confi = track_confi


        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.image_mode,
                                max_num_hands=self.num_hands,
                                min_detection_confidence=self.detec_confi,
                                min_tracking_confidence=self.track_confi 
                            )

        self.mpDraw = mediapipe.solutions.drawing_utils
        # static image mode (false) -> sometimes detect, sometimes track based on confidence level
        # (true) -> it will detect continously, which make it slow



    def find_hands(self, image, draw=True):
        # hands class only works on RGB images
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            # below loop is for multiple hands
            for i in self.results.multi_hand_landmarks:
                if(draw):
                    self.mpDraw.draw_landmarks(imageRGB, i, self.mpHands.HAND_CONNECTIONS)
        return imageRGB    

        
    def find_position(self, image, handno=0):
        self.landmarks = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handno]
            for id, mark in enumerate(myHand.landmark):
                height, width, channel = image.shape
                cx, cy = int(mark.x * width), int(mark.y * height)
                self.landmarks.append([id, cx, cy])
        
        return self.landmarks

    def fingers_up(self):
        # finger is up
        #  
        tipIds = [8, 12, 16, 20]
        fingers = []
        # handle thumb saperately
        if(self.landmarks[4][1] > self.landmarks[3][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        for i in tipIds:
            if(self.landmarks[i][2] < self.landmarks[i-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def find_distance(self, pts1, pts2, img, draw=True, r=15, t=3):
        x1, y1 = self.landmarks[pts1][1:]
        x2, y2 = self.landmarks[pts2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255,0,255), t)
            cv2.circle(img, (x1, y1), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

# def main():
#     # to calculate frame rate
#     prevtime = 0
#     currtime = 0

    
#     # read video stream
#     cap = cv2.VideoCapture(0)
#     detector = HandTracker()

#     while(True):
#         # extract image from video
#         success, image = cap.read()

#         imageRGB = detector.find_hands(image)  
        
#         print(detector.find_position(imageRGB))
        
#         currtime = time.time()
#         fps = 1 / (currtime - prevtime)
#         prevtime = currtime

#         cv2.putText(imageRGB, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
#         cv2.imshow("image", imageRGB)


#         # press escape key to quit
#         if(cv2.waitKey(1) == 27):
#             cap.release()
#             cv2.destroyAllWindows()
#             break





# if __name__ == "__main__":
#     main()