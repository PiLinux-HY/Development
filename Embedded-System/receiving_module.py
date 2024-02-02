import time, json, ssl
import paho.mqtt.client as mqtt

ENDPOINT = "본인의 엔드포인트"
THING_NAME = 'raspi'
CERTPATH =  "/home/pi/aws/raspi.cert.pem" # cert파일 경로
KEYPATH = "/home/pi/aws/raspi.private.key" # key 파일 경로
CAROOTPATH = "/home/pi/aws/root-CA.crt" # RootCaPem 파일 경로
TOPIC = 'test' #주제

def on_connect(mqttc, obj, flags, rc):
  if rc == 0: # 연결 성공
    print('connected')
    
def on_message(mqttc, obj, msg):
  print(msg.topic+":"+str(msg.payload))

def on_subscribe(mqttc, obj, mid, granted_qos):
  print("Subscribed: "+TOPIC)

try:
  mqtt_client = mqtt.Client(client_id=THING_NAME)
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  mqtt_client.on_subscribe = on_subscribe
  
  mqtt_client.tls_set(CAROOTPATH, certfile= CERTPATH, keyfile=KEYPATH, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
  mqtt_client.connect(ENDPOINT, port=8883)
  mqtt_client.subscribe(TOPIC)
  mqtt_client.loop_start()
  while(1):
      time.sleep(2)

except KeyboardInterrupt:
    pass
  
mqtt_client.disconnect()
print(end='\n')