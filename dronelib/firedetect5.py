import cv2
import numpy as np 
import time

class fireDetect:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.fire_cascade = cv2.CascadeClassifier('/home/hualtech/Desktop/libraries/dronekit2/fire_detection.xml')
        self.status = False
        self.start_time = 0
        self.stop_time = 0

    def open_cam(self):
        while True:
            ret , frame = self.cap.read()
            if ret:
                cv2.imshow("Frame" , frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    def take_photo(self):
        self.cap = cv2.VideoCapture(0)
        
        ret , frame = self.cap.read()
        if ret:
            cv2.imshow("Frame" , frame)
            if cv2.waitKey(0) & 0xFF == ord("q"):
                pass
        else:
            print("Görüntü verisi yok.")

    def take_video(self , videoname , delay):
        self.cap = cv2.VideoCapture(0)
        val = time.time()
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        writer = cv2.VideoWriter(f"{videoname}.mp4" , cv2.VideoWriter_fourcc(*'XVID'),25,(width,height))
        while time.time() - val <= delay:
            ret , frame = self.cap.read()
            if ret:
                writer.write(frame)
            else:
                print("Kayıt tamamlandı.")
                writer.release()
    
    def show_video(self , videoname):
        self.cap = cv2.VideoCapture(f"{videoname}.mp4")
        print("Genişlik :" , self.cap.get(3))
        print("Yükseklik :" , self.cap.get(4))
        start_time = time.time()
        if self.cap.isOpened() == False: # isOpened ifadesi video yada fotoğrafın olup olmadıpını kontrol eder.
            print("Video açılmadı.")
        else:
            while True:
                ret , frame = self.cap.read()
                if ret:
                    time.sleep(0.017)
                    cv2.imshow("Frame" , frame)
                else:
                    break
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        stop_time = time.time() - start_time
        print(f"Geçen zaman : {stop_time}")
    
    def detect_fire(self):
        ret , frame = self.cap.read()
        if ret:
            rect = self.fire_cascade.detectMultiScale(frame , scaleFactor = 1.045 , minNeighbors = 5)
            for (x , y , w , h) in rect:
                    cv2.rectangle(frame , (x,y) , (x+w,y+h) , (255,255,255) , 4)
            #print(f"Tespit sayısı : {len(rect)} , Status : {self.status}")
            if (len(rect) > 0) and not(self.status):
                self.status = True
                self.start_time = time.time()
            elif (self.stop_time - self.start_time) > 10:
                self.status = False
                self.start_time = self.stop_time
            else:
                pass
            cv2.imshow("Frame" , frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                pass
            self.stop_time = time.time()
            return self.status
        else:
            pass
    
    def stretch_brightness(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            ret , frame = self.cap.read()
            if ret:
                val = 100 # 1.25 1.5 1.75
                xp = [0, 64, 128, 192, 255]
                fp = [0, 16, 128 - (val*1.25) , 240 - (val*1.5) , 255 - (val*1.75)]
                x = np.arange(256)
                table = np.interp(x, xp, fp).astype('uint8')
                image = cv2.LUT(frame , table)
                rect = self.fire_cascade.detectMultiScale(image , scaleFactor = 1.045 , minNeighbors = 5)
                for (x , y , w , h) in rect:
                    cv2.rectangle(image , (x,y) , (x+w,y+h) , (255,255,255) , 5)
                cv2.imshow("Frame" , image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    def close_cam(self):
        self.cap.release()
        cv2.destroyAllWindows()