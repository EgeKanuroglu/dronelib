from dronekit import connect, VehicleMode, LocationGlobalRelative
import pymongo as pm
import time
from datetime import datetime
from bson.objectid import ObjectId
import os

import firedetectV1R1 as fd1
fd = fd1.fireDetect()

print("Başlangıç verildi.")
#value = 'dev/ttyAMA0'
value = '127.0.0.1:14550'
iha = connect(value , wait_ready=True , baud = 57600)

start_time = time.time()
clienturl = "mongodb+srv://useradmin:erenege345E@owldb.inzdrty.mongodb.net/?retryWrites=true&w=majority"
serino = "123asd123"

# pitch roll 1.5 , -1.5  yaw 3 , -3
pitch_val = 180 / 3
roll_val = 180 / 3
yaw_val = 360 / 6

months = ["Ocak" , "Şubat" , "Mart" , "Nisan" , "Mayıs" , "Haziran" , "Temmuz" , "Ağustos" , "Eylül" , "Ekim" , "Kasım" , "Aralık"]

date = datetime.now()
start_date = f"{date.day} {months[date.month-1]} {date.year}"
start_dtime = f"{date.hour-1}:{date.minute}"
place = "Zeytinburnu"
detect_status = True

droneval = {
    "serial_no" : serino,
    
    "gps_lat" : 28.9382347,
    "gps_lon" : 41.0369696,
    "gps_alt" : 0,

    "old_lat" : 12.2,
    "old_lon" : 12.2,

    "pitch" : 22,
    "roll" : 22,
    "yaw" : 22,
    "old_yaw" : 22,

    "battery_level" : 23,
    "flight_time" : 0,
    "total_flight_time" : 0,
    
    "mode" : "none",
    "system_status" : "standby",
    "message" : "none",
    "velocity" : "0",

    "fire_lat" : 12.2,
    "fire_lon" : 12.2,
    "latest_status" : False,
    "find_time" : "7 Şubat 2023 14:53"
}

flightrecords = {
  "serial_no": serino,
  
  "altitudes": [10,20,30,40,50],
  
  "datetime": "4 Şubat 2023",
  "location_time": "Zeytinburnu 12:17 - 12:18",
  
  "datetime2": "10 Mart 2023",
  "location_time2": "Dikilitaş 12:30 - 15:20",
  
  "datetime3": "5 Mart 2023",
  "location_time3": "Yeşiltepe 15:30 - 16:20",
  
  "datetime4": "25 Şubat 2023",
  "location_time4": "Sümer 10:30 - 12:25",
  
  "datetime5": "10 Şubat 2023",
  "location_time5": "Çırpıcı 12:25 - 15:36",
  
  "altitudes1": "10000",
  "altitudes2": "18000",
  "altitudes3": "15000",
  "altitudes4": "13000",
  "altitudes5": "12000",
  
}

def check_database():
    global clienturl
    global myclient
    global db

    global drone_coll
    global flight_rec_coll
    global user_coll
    global waypoint_coll

    global start_time
    global latest_time

    try:
        myclient = pm.MongoClient(clienturl)
    except Exception:
        raise Exception("Veri tabanına bağlanılamadı.")
    else:
        print("MongoDB Bağlantısı " + "✔️")
        db = myclient["owldb"]

        drone_coll = db["dronevalues"]
        flight_rec_coll = db["flightrecords"]
        user_coll = db["users"]
        waypoint_coll = db["waypoints"]

        latest_time = drone_coll.find_one({"serial_no" : serino})["total_flight_time"]
    
def check_battery():
    global iha
    # (iha.battery.voltage < 5 or iha.battery.current < 3) pixhawk için
    # iha.battery.level < 20 simülasyon için
    if iha.battery.level < 20:
        raise Exception("Uçuş yapmak için yeterli güç bulunmuyor.")
    else:
        print("Batarya Kontrolü " + "✔️")

def check_gps():
    global iha
    if iha.location.global_relative_frame.lat == 0:
        raise Exception("GPS verisi bulunamadı.")
    else:
        print("GPS Kontrolü " + "✔️")

def check_armable():
    global iha
    counter = 0
    #iha.is_armable = True
    while iha.is_armable is not True:
        print("İHA arm durumu bekleniyor...")
        if counter > 5:
            raise Exception("İHA arm edilebilir durumda değil.")
        counter += 1
        time.sleep(1)

    iha.mode = VehicleMode("GUIDED")
    iha.armed = True
    while iha.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(0.5)

    print("İHA Armable Durumu " + "✔️") 

def check_camera(cam_ind):
    try:
        fd.set_cam(cam_ind)
    except Exception as ex:
        raise Exception(ex)
    else:
        print("Kamera Kontrolü " + "✔️")

def check_home_location():
    pass

def create_set(val):
    command = {
        "$set" : val
    }
    return command

def update_drone_values(msg):
    global start_time
    global droneval
    global latest_time
    global drone_coll

    gps = iha.location.global_relative_frame
    battery = iha.battery
    attitude = iha.attitude

    stop_time = time.time()
    total_val = int(stop_time + latest_time - start_time)
    val = int(stop_time - start_time)
    
    droneval["gps_lat"] = gps.lat
    droneval["gps_lon"] = gps.lon
    droneval["gps_alt"] = gps.alt

    droneval["pitch"] = int(abs(attitude.pitch * pitch_val))
    droneval["roll"] = int(abs(attitude.roll * roll_val))
    droneval["yaw"] = int(abs(attitude.yaw * yaw_val))

    droneval["battery_level"] = battery.level
    droneval["flight_time"] = val
    droneval["total_flight_time"] = total_val

    droneval["mode"] = iha.mode.name
    droneval["system_status"] = iha.system_status.state
    droneval["message"] = msg

    speed = str(((abs(iha.velocity[0]) + abs(iha.velocity[1]) + abs(iha.velocity[2])) * 3600) / 1000) # km/saat cinsine çevirdik
    droneval["velocity"] = f"{speed[0:4]}"

    drone_coll.update_one({"serial_no" : serino} , create_set(droneval))

def update_fire_values():
    global droneval

    fd.set_cascade("fire_detection")
    detect = fd.detect_fire()

    if detect and fd.detect_lock:
        droneval["fire_lat"] = iha.location.global_relative_frame.lat
        droneval["fire_lon"] = iha.location.global_relative_frame.lon
        droneval["fire_status"] = True
        drone_coll.update_one({"serial_no" : serino} , create_set(droneval))
        fd.detect_lock = False
        print("İşaret atıldı. Beklemeye alındı.")
    elif (detect == False) and (fd.detect_lock == False):
        fd.detect_lock = True
        print("Tespit aktif.")
    else:
        pass

def loop(message):
    global droneval
    update_drone_values(message)
    update_fire_values()

def finish_loop(message):
    iha.close()

    droneval["mode"] = iha.mode.name
    droneval["system_status"] = iha.system_status.state
    droneval["message"] = message

    drone_coll.update_one({"serial_no" : serino} , create_set(droneval))

    date = datetime.now()
    stop_dtime = f"{date.hour-1}:{date.minute}"
    
    flightrecords["datetime"] = f"{start_date}"
    flightrecords["location_time"] = f"{place} {start_dtime} - {stop_dtime}"

    flight_rec_coll.update_one({"serial_no" : serino} , create_set(flightrecords))

    myclient.close()
    fd.close_cam()

class myDroneKit:
    def __init__(self):
        self.mainlock = True
        try:
            check_database()
            check_battery()
            check_gps()
            check_armable()
            check_camera()
        except Exception as ex:
            print(ex) 
            self.mainlock = False
        else:
            self.homeloc = iha.location.global_relative_frame

            self.battery_home = 20
            self.battery_land = 10

            self.takeoff_tol = 0.9 # yüzde
            self.home_tol = 5 # metre
            self.land_tol = 0.5 # metre
            self.air_tol = 0.2 # metre
            self.mode = "land"
            
    def take_off(self , high):
        global iha
        if self.mainlock and self.mode == "land" and iha.armed:
            self.mode = "guided"
            iha.simple_takeoff(high)
            while iha.location.global_relative_frame.alt < high * self.takeoff_tol:
                loop("Kalkış yapılıyor...")

    def go_location(self , x , y , z):
        global iha
        if self.mainlock:
            location = LocationGlobalRelative(x , y , z)
            iha.simple_goto(location)
            time.sleep(1)
            while iha.airspeed > self.air_tol:
                loop("Belirtilen konuma gidiliyor...")
                if iha.airspeed <= self.air_tol:
                    break

    def go_waypoint(self):
        global iha # BAKIMDA
        if self.mainlock:
            pass

    def set_waypoint(self):
        global iha # BAKIMDA
        if self.mainlock:
            pass
    
    def set_home(self):
        global iha # BAKIMDA
        if self.mainlock:
            loc = iha.location.global_frame
            val = [loc.lat , loc.lon , loc.alt]
            drone_coll.update_one({"_id" : 7} , create_set("home_location" , [val[0] , val[1] , val[2]]))


    def go_home(self):
        global iha       # BAKIMDA
        if self.mainlock:
            #location = LocationGlobalRelative(self.homeloc.lat , self.homeloc.lon , self.homeloc.alt + self.home_tol)
            loc = LocationGlobalRelative(iha.home_location.lat , iha.home_location.lon , iha.home_location.alt)
            iha.simple_goto(loc)
            time.sleep(1)
            while iha.airspeed > self.air_tol:
                loop("Geri dönüş yapılıyor...")
                if iha.airspeed <= self.air_tol:
                    break

    def land(self):
        global iha
        if self.mainlock:
            self.mode = "land"
            iha.mode = VehicleMode("LAND")
            while iha.location.global_relative_frame.alt > self.land_tol:
                loop("İniş yapılıyor...")

    def finish(self):
        finish_loop("Cihaz kapatıldı.")