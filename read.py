import serial, sys, time, commands, re, os
import logging
import paho.mqtt.client as paho
import time
#reload(sys)
#sys.setdefaultencoding('utf8')
MQTT = {
    'default': {
        'NAME': os.environ.get('MQTT_NAME', ''),
        'USER': os.environ.get('MQTT_USER', ''),
        'PASSWORD': os.environ.get('MQTT_PASSWORD', ''),
        'HOST': os.environ.get('MQTT_HOST', 'mqtt.cmmc.io'),
        'port': os.environ.get('MQTT_PORT', 1883),
        'TOPIC_1': os.environ.get('MQTT_TOPIC_1', 'CMMC/nat1/espnow'),
        'TOPIC_2': os.environ.get('MQTT_TOPIC_2', 'CMMC/nat1/espnow'),
    }
}


def on_publish(client, userdata, mid):
    print("on_publish")
    print("mid: "+str(mid))
    print userdata
    pass

client = paho.Client()
client.on_publish = on_publish
client.connect(MQTT['default']['HOST'], MQTT['default']['PORT'])
client.loop_start()

device = None
baud = 9600

if not device:
    devicelist = commands.getoutput("ls /dev/ttyAMA*")
    if devicelist[0] == '/':
        device = devicelist
    if not device:
        print "Fatal: Can't find usb serial device."
        sys.exit(0);
    else:
        print "Success: device = %s"% device

ser = serial.Serial(
    port=device,
    baudrate=baud,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#https://stackoverflow.com/a/27628622
def readline(a_serial, eol=b'\r\n'):
    leneol = len(eol)
    line = bytearray()
    while True:
        c = a_serial.read(1)
        # print c
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return (line)

def str2hexstr(line):
  return " ".join(hex(ord(n)) for n in line)

print "reading..."
while True:
    try:
        line = readline(ser)
        line_str = bytes(line)
        line_hex = str2hexstr(line_str)
        # print "len = %d" % len(line_str)
        # b_header = line[0:2]
        # b_mac1 = line[2:8]
        # b_mac2 = line[8:14]
        # msglen = line[14]
        # msg = line[15:15+msglen]
        # print str2hexstr(bytes(b_header))
        # print str2hexstr()
        # print msglen
        # print str2hexstr(bytes(msg))
        # print line_str
        print str2hexstr(line_str)
        (rc, mid) = client.publish(MQTT['default']['MQTT_TOPIC_1'], line, qos=0)
        (rc, mid) = client.publish(MQTT['default']['MQTT_TOPIC_2'], line, qos=0)
    except Exception as e:
        print e
    except KeyboardInterrupt:
        print "closing serial port..."
        ser.close()
        sys.exit()
    finally:
        pass
