import pymongo as pm # kütüphanemizi ekledik
from datetime import datetime
# client url ini aldık
clienturl = "mongodb+srv://useradmin:erenege345E@owldb.inzdrty.mongodb.net/?retryWrites=true&w=majority"
myclient = pm.MongoClient(clienturl) # bağlantımızı sağladık
print(myclient.list_database_names()) # veri tabanı isimlerini listeledik

mydb = myclient["owldb"] # node-app veri tabanına ulaştık
print(mydb.list_collection_names())

serino = "123asd123"
months = ["Ocak" , "Şubat" , "Mart" , "Nisan" , "Mayıs" , "Haziran" , "Temmuz" , "Ağustos" , "Eylül" , "Ekim" , "Kasım" , "Aralık"]

date = datetime.now()
start_date = f"{date.day} {months[date.month+1]} {date.year}"
start_dtime = f"{date.hour-1}:{date.minute}"
place = "Zeytinburnu"

date = datetime.now()

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
    "fire_status" : False,
    "possibility" : 0,
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

users = {
    "serial_no" : serino,
    "username" : "kaan",
    "password" : "kaan31",
    "register_date" : "22 Aralık 2022",
    "latest_login_date" : "7 Şubat 2023"
}

waypoints = {
    "serial_no" : serino,
    "wp_lat" : 12.2,
    "wp_lon" : 12.2,
    "wp_alt" : 12.2
}

firepoints = {
    "serial_no" : serino,
    "fire_lat" : 12,
    "fire_lon" : 12,
    "last_status" : False, # True aktif yangın , False önlendi
    "find_time" : "7 Şubat 2023 14:53"
}

totalvals = [droneval , flightrecords , users , waypoints]
counter = 0

for val in mydb.list_collection_names():
    mycoll = mydb[val]
    result = mycoll.delete_many({}) # farklı değerler var ise hepsini temizliyoruz
    print(f"{result.deleted_count} adet kayıt silindi.")
    result = mycoll.insert_one(totalvals[counter])
    counter += 1

print("Belirtilen kayıtlar yüklendi.")
myclient.close()