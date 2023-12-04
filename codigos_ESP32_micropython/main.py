from machine import Pin, ADC, I2C
from time import sleep
from ESP_CONNECTION import *
from umqtt.simple import *
from bme680 import *



mqtt_broker    = "192.168.1.4"
mqtt_topic     = "MOSQUITTO"
mqtt_client_id = "esp32_client_taller_iot"



def run():
    
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    bme = BME680_I2C(i2c=i2c)
    
    pot = ADC( Pin(35) )
    
    
    time_to_send = 10
    
    #CONECTIVIDAD CON LA RED
    wifi               = ESP32_CONNECTION()
    if wifi.status():
        print("ya esta conectado siii")
    else:
        status_wifi        =  wifi.connect()
    
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_broker)
    
    #client.setSSID_PASSW("SSID","PASSWORD")
    client.connect()
    
    
    
   
    while True:
        temp = str(round(bme.temperature, 2)) + ' C'
        hum = str(round(bme.humidity, 2)) + ' %'
        pres = str(round(bme.pressure, 2)) + ' hPa'
        gas = str(round(bme.gas/1000, 2)) + ' KOhms'
        
        
        potvalue = pot.read_u16()*3.3/65535.0
        print("potenciometro 1: ",potvalue)
        
        print('Temperature:', temp)
        print('Humidity:', hum)
        print('Pressure:', pres)
        print('Gas:', gas)
        print('-------')
        
        
        if time_to_send == 0:
            time_to_send = 11
            try:
                str_pot = "{:.1f}".format(potvalue)
                client.publish("iSebasHOME/POT1",str(potvalue) )
                client.publish("iSebasHOME/TEMP",temp )
                client.publish("iSebasHOME/HUM",hum )
                client.publish("iSebasHOME/PRES",pres )
                client.publish("iSebasHOME/GAS",gas )
            except:
                print("Error MQTT")
        
        time_to_send -= 1
        sleep(1)
        
        
                    

if __name__ == "__main__":
    run()