import cv2
import time
import os
import numpy as np

class fireDetect:
    def __init__(self):
        self.start_time = time.time()
        self.stop_time = 0
        self.lock = True
        self.detect = False
        self.detect_lock = True

    def set_cam(self , cam_index):
        try:
            self.cap = cv2.VideoCapture(cam_index)
            ret , frame = self.cap.read()
            if ret == False:
                raise Exception("Belirtilen kamera bulunamadı.")
            else:
                pass
        
        except Exception:
            raise Exception("Belirtilen kamera bulunamadı.")
        
        else:
            self.video = cv2.VideoCapture(cam_index)

    def set_cascade(self , cascade_name):
        try:
            try:
                ret , frame = self.cap.read()
            except Exception:
                raise Exception("Kamera indeksi belirtilmedi.")
            else:
                try:
                    self.cascade = cv2.CascadeClassifier(f"/home/hualtech/Desktop/libraries/fire_detection/database/{cascade_name}.xml")
                    rect = self.cascade.detectMultiScale(frame , scaleFactor = 1.045 , minNeighbors = 5)
                except Exception:
                    raise Exception("Belirtilen cascade bulunamadı.")
                else:
                    self.cascade_name = cascade_name

        except Exception as ex:
            raise Exception(ex)
        else:
            pass

    def open_cam(self):
        try:
            ret , frame = self.cap.read()
        except Exception:
            raise Exception("Kamera indeksi belirtilmedi.")
        else:
            if ret:
                cv2.imshow("WebCam" , frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.lock = False
            else:
                print("Görüntü verisi yok.")
                self.lock = False
                
    def take_photo(self):
        try:
            ret , frame = self.cap.read()
        except Exception:
            raise Exception("Kamera indeksi belirtilmedi.")
        else:
            index = len(os.listdir("output/photo")) + 1
            if ret:
                cv2.imwrite(f"output/photo/photo{index}.png" , frame)
            else:
                print("Görüntü verisi yok.")

    def take_video(self , delay):
        try:
            ret , frame = self.cap.read()
        except Exception:
            raise Exception("Kamera indeksi belirtilmedi.")
        else:
            self.start_time = time.time()

            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
            index = len(os.listdir("/home/hualtech/Desktop/libraries/fire_detection/output/video/")) + 1
            writer = cv2.VideoWriter(f"/home/hualtech/Desktop/libraries/fire_detection/output/video/video{index}.mp4" , cv2.VideoWriter_fourcc(*'XVID'),25,(width,height))
            while time.time() - self.start_time <= delay:
                ret , frame = self.cap.read()
                if ret:
                    writer.write(frame)
                    cv2.imshow(f"Recording..." , frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        pass
                else:
                    print("Kayıt tamamlandı.")
                    writer.release()
    
    def show_photo(self , photoname):
        try:
            img = cv2.imread(f"output/photo/{photoname}.png" , 1)
            cv2.imshow("Photo" , img)
            if cv2.waitKey(0) & 0xFF == ord("q"):
                pass
        except Exception:
            raise Exception("Fotoğraf bulunamadı.")
        else:
            pass

    def show_video(self , videoname):
        try:
            self.video = cv2.VideoCapture(f"/home/hualtech/Desktop/libraries/fire_detection/output/video/{videoname}.mp4")
            if self.video.isOpened() == False:
                raise Exception("Video bulunamadı.")
        except Exception as ex:
            raise Exception(ex)
        else:
            print("Genişlik :" , self.video.get(3))
            print("Yükseklik :" , self.video.get(4))
        
            self.start_time = time.time()
            while self.lock:
                ret , frame = self.video.read()
                if ret:
                    cv2.imshow("Frame" , frame)
                    time.sleep(0.027)
                else:
                    self.lock = False
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.lock = False

            self.stop_time = time.time()   
            spend_time = self.stop_time - self.start_time
            print(f"Geçen zaman : {str(spend_time)[0:5]}")
    
    def detect_fire(self):
        try:
            ret , frame = self.cap.read()
            if ret == False:
                raise Exception("Kamera indeksi belirtilmedi.")
            else:
                pass
        except Exception:
            raise Exception("Kamera indeksi belirtilmedi.")
        else:
            if ret:
                try:
                    rect = self.cascade.detectMultiScale(frame , scaleFactor = 1.045 , minNeighbors = 5)
                except Exception:
                    raise Exception("Cascade belirtilmedi.")
                else:   
                    for (x , y , w , h) in rect:
                        cv2.rectangle(frame , (x,y) , (x+w,y+h) , (255,255,255) , 3)
                    
                    if (len(rect) > 0) and (self.detect == False):
                        self.detect = True
                        self.start_time = time.time()
                    
                    if self.stop_time - self.start_time > 10:
                        self.detect = False
                        self.start_time = self.stop_time

                    cv2.imshow(self.cascade_name , frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.lock = False
                    
                    self.stop_time = time.time()
                    return self.detect
            else:
                print("Görüntü verisi yok.")
                self.lock = False
    
    def close_cam(self):
        try:
            self.cap.release()
            cv2.destroyAllWindows()
        except Exception:
            pass
        else:
            pass