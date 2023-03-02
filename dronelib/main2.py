import dronekitlibV1R4 as dk
dronekit = dk.myDroneKit()
dronekit.take_off(10)
dronekit.go_location(-35.36279225 , 149.16515750 , 10)
dronekit.go_location(-35.36327156 , 149.16523138 , 10)
dronekit.land()
dronekit.finish()
