import logging
import threading
import cv2
import numpy as np

USE_FAKE_PI_CAMERA = False  # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_PI_CAMERA:
    from .camera import Camera  # For running app
else:

    from .pi_camera import Camera  # For running Raspberry Pi

log = logging.getLogger(
    __name__)  # Creates a logger instance, we use it to log things out


class OpenCVController(object):

    def __init__(self):
        self.current_shape = [False, False, False]
        print('OpenCV controller initiated')

    def process_frame(self):
        camera = Camera()
        image = camera.get_frame()

        jpg_to_np = np.frombuffer(image, np.uint8)

        imgDec = cv2.imdecode(jpg_to_np, cv2.COLOR_RGB2BGR)

        hsvFrame = cv2.cvtColor(imgDec, cv2.COLOR_BGR2HSV)

        # range for lower red
        lr1 = np.array([0, 120, 70])
        lr2 = np.array([10, 255, 255])
        lr_mask = cv2.inRange(hsvFrame, lr1, lr2)

        # range for upper red
        ur1 = np.array([170, 120, 70])
        ur2 = np.array([180, 255, 255])
        ur_mask = cv2.inRange(hsvFrame, ur1, ur2)

        red_mask = lr_mask + ur_mask

        # range for lower blue
        lb1 = np.array([68, 120, 0])
        lb2 = np.array([70, 255, 255])
        lb_mask = cv2.inRange(hsvFrame, lb1, lb2)

        # range for upper blue
        ub1 = np.array([90, 120, 5])
        ub2 = np.array([130, 255, 255])
        ub_mask = cv2.inRange(hsvFrame, ub1, ub2)

        blue_mask = lb_mask + ub_mask



        # blue contours
        blue_cont, r_hierachy = cv2.findContours(ub_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        for blue_cont in blue_cont:
            area = cv2.contourArea(blue_cont)
            if (area > 3000):
                b_x, b_y, b_w, b_h = cv2.boundingRect(blue_cont)

                poly = cv2.approxPolyDP(blue_cont, 0.01 * cv2.arcLength(blue_cont, True), True)
                # print(poly)
                test = len(poly)
                cv2.drawContours(imgDec, [blue_cont], 0, (0, 255, 0), 5)
                if len(poly) == 3:
                    cv2.rectangle(imgDec, (b_x, b_y), (b_x + 150, b_y - 50), (0, 255, 0), -1)
                    cv2.putText(imgDec, "TRIANGLE SHAPE", (b_x, b_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                                thickness=1)
                elif len(poly) > 12:
                    cv2.rectangle(imgDec, (b_x, b_y), (b_x + 150, b_y - 50), (0, 255, 0), -1)
                    cv2.putText(imgDec, "CIRCLE SHAPE", (b_x, b_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                                thickness=1)
                elif len(poly) == 4:
                    cv2.rectangle(imgDec, (b_x, b_y), (b_x + 150, b_y - 50), (0, 255, 0), -1)
                    cv2.putText(imgDec, "SQUARE SHAPE", (b_x, b_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                                thickness=1)

                # red contours
                red_cont, r_hierachy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

                for red_cont in red_cont:
                    area = cv2.contourArea(red_cont)
                    if (area > 1000):
                        r_x, r_y, r_w, r_h = cv2.boundingRect(red_cont)
                        #print(r_x)
                        #print(r_y)
                        cv2.rectangle(imgDec, (r_x, r_y), (r_x + r_w, r_y + r_h), (0, 0, 255), 2)
                        cv2.rectangle(imgDec, (r_x, r_y), (r_x + 150, r_y - 50), (0, 0, 255), -1)
                        cv2.putText(imgDec, "MARK", (r_x, r_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),thickness=1)
                        if(r_x == 1980):
                            self.current_shape = [True, True, False]
                        elif(r_x == 2980):
                            self.current_shape = [False,True,True]
                        elif (r_x < 1980):
                            self.current_shape=[True,False,False]
                        elif(r_x > 1980 and r_x < 2980):
                            self.current_shape = [False, True, False]
                        elif(r_x > 2980):
                            self.current_shape = [False, False, True]

        frame = cv2.imencode('.jpg', imgDec)[1].tobytes()

        return frame

        image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

        image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_current_shape(self):
        return self.current_shape
