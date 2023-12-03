import network
from time import sleep


SSID = ""
PASS = ""


class ESP32_CONNECTION():
    
    def __init__(self):
        
        self._ssid = SSID
        self._pass = PASS
        
        # Crear una instancia de la clase WLAN
        self.wlan = network.WLAN(network.STA_IF)
    
    def setSSID_PASSW(self, newSSID=SSID, newPASS=PASS):
        self._ssid = newSSID
        self._pass = newPASS
    
    def status(self):
        status = self.wlan.isconnected()
        print("estado de la conexion: ", status)
        return status
    
    def disconnect(self):
        self.wlan.disconnect()
    
    def connect(self):
        
        
        # Conectar a la red Wi-Fi
        self.wlan.active(True)
        self.wlan.connect(self._ssid, self._pass)
        
        # Esperar a que se establezca la conexión
        time_out = 20
        while not self.wlan.isconnected():
            time_out -= 1
            sleep(1)
            if time_out == 0:
                print("Error Trying Connection")
                return False
        print("Conexion establecida con la red: \n\n")
        print("\t\t\tSSID: ",self._ssid,"\n\n")
        return True
    