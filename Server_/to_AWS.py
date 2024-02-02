import time, json, ssl
import paho.mqtt.client as mqtt

ENDPOINT = "a227tuxatcxi09-ats.iot.ap-northeast-2.amazonaws.com"
THING_NAME = 'JJONG'
CERTPATH =  "/home/piLinux/JJONG.cert.pem" 
KEYPATH = "/home/piLinux/JJONG.private.key" 
CAROOTPATH = "/home/piLinux/root-CA.crt" 
TOPIC = 'test' 

def on_connect(mqttc, obj, flags, rc):
  if rc == 0: 
    print('connected!!')

try: 
  mqtt_client = mqtt.Client(client_id=THING_NAME)
  mqtt_client.on_connect = on_connect
  mqtt_client.tls_set(CAROOTPATH, certfile= CERTPATH, keyfile=KEYPATH, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
  mqtt_client.connect(ENDPOINT, port=8883)
  mqtt_client.loop_start()
  
  i=0
  while True: 
    payload = json.dumps({'action': i*0.1}) 
    mqtt_client.publish('test', payload, qos=1) 
    i=i+1 
    time.sleep(2)

except KeyboardInterrupt:
    pass
  
mqtt_client.disconnect()
print(end='\n')