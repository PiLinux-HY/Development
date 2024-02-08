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
    print('connected!!')

try: 
  mqtt_client = mqtt.Client(client_id=THING_NAME)
  mqtt_client.on_connect = on_connect
  mqtt_client.tls_set(CAROOTPATH, certfile= CERTPATH, keyfile=KEYPATH, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
  mqtt_client.connect(ENDPOINT, port=8883)
  mqtt_client.loop_start()
  
  i=0
  while True: 
    payload = json.dumps({'action': i*0.1}) #메시지 포맷
    mqtt_client.publish('test', payload, qos=1) #메시지 발행
    i=i+1 
    time.sleep(2)

except KeyboardInterrupt:
    pass
  
mqtt_client.disconnect()
print(end='\n')