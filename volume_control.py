
import paho.mqtt.client as mqtt
from pycaw.pycaw import AudioUtilities

# Périphérique audio Windows par défaut
device = AudioUtilities.GetSpeakers()

# Volume initial
print(f"Volume actuel : {device.volume_percent:.0f}%")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connecte au broker MQTT")
        client.subscribe("hand/volume")
        print("En attente du volume...")
    else:
        print("Erreur de connexion :", reason_code)

def on_message(client, userdata, msg):
    try:
        volume = float(msg.payload.decode())

        # Volume compris entre 0 et 100
        volume = max(0, min(100, volume))

        # Modifier le volume réel de Windows
        device.volume_percent = volume

        print(f"Volume Windows : {volume:.0f}%")

    except ValueError:
        print("Valeur de volume invalide")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Arret du controle du volume")
finally:
    client.disconnect()
