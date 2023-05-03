import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
from imutils.video import VideoStream
import time

class MyDetector():
  IMG_SIZE = (34, 26)


  def crop_eye(self, img, eye_points):
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    w = (x2 - x1) * 1.2
    h = w * self.IMG_SIZE[1] / self.IMG_SIZE[0]

    margin_x, margin_y = w / 2, h / 2

    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(int)

    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    return eye_img, eye_rect

  def webcam(self, state, state_changed):
    COUNTER = 0
    # TOTAL = 0
    # now_time = time.localtime().tm_sec + time.localtime().tm_min * 60 + time.localtime().tm_hour * 3600
    recent_blink = time.time()
    
    blink_time = 0
    acc_time = 0

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    model = load_model('models/blink-classify.h5')
    model.summary()
    window = []

    def time_window(sec):
      if sec < 60:
        window.append(sec)
        return window
      else:
        window.append(sec)
        if window[0] < sec - 60:
          for i in range(len(window)):
            if window[i] < sec - 60:
              del window[0]
            else:
              break
          # print(window)
          return window
        else:
          # print(window)
          return window


    # webcam
    print("[INFO] camera sensor warming up...")
    vs = VideoStream(0).start()
    time.sleep(2.0)

#    cv2.moveWindow('result', 400, 400)  # 윈도우 위치 조정

    while True:
      img_ori = vs.read()
      img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

      img = img_ori.copy()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      faces = detector(gray)

      for face in faces:
        shapes = predictor(gray, face)
        shapes = face_utils.shape_to_np(shapes)

        eye_img_l, eye_rect_l = self.crop_eye(gray, eye_points=shapes[36:42])
        eye_img_r, eye_rect_r = self.crop_eye(gray, eye_points=shapes[42:48])

        eye_img_l = cv2.resize(eye_img_l, dsize=self.IMG_SIZE)
        eye_img_r = cv2.resize(eye_img_r, dsize=self.IMG_SIZE)
        eye_img_r = cv2.flip(eye_img_r, flipCode=1)

        # cv2.imshow('l', eye_img_l)
        # cv2.imshow('r', eye_img_r)

        eye_input_l = eye_img_l.copy().reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.
        eye_input_r = eye_img_r.copy().reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.

        pred_l = model(eye_input_l)
        pred_r = model(eye_input_r)

        print('r: ', pred_r[0])
        print('l: ', pred_l[0])
        # visualize
        state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
        state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'
        
        state_l = state_l % pred_l
        state_r = state_r % pred_r
        '''
        if state_r[0] == '-' and state_l[0] == '0':
          print('left')
        elif state_r[0] == '0' and state_l[0] == '-':
          print('right')
        '''
        
        if state_r[0] == '-' and state_l[0] == '-':
          COUNTER += 1
        else:
          if COUNTER >= 1:
            # TOTAL += 1
            # blink_time = time.localtime().tm_sec + time.localtime().tm_min * 60 + time.localtime().tm_hour * 3600
            # acc_time = blink_time - now_time
            
            elapsed_time = time.time()-recent_blink
            
            recent_blink = time.time()

            # print(elapsed_time)
            
            if elapsed_time<0.5:
              print("double blink")

            
            li = time_window(acc_time)
            # print("blink count: {}, measure time: {} ".format(len(li), acc_time))
            if acc_time > 60:
              state_changed.emit('{}'.format(str(len(li))))

          # reset the eye frame counter
          COUNTER = 0

        cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255), thickness=2)
        cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255), thickness=2)

        cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

      cv2.imshow('result', img)

      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break
