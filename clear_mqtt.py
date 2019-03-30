import getopt
import paho.mqtt.client as paho
import sys

final_mid = 0


def on_connect(mosq, userdata, rc):
    if userdata == True:
        print("rc: "+str(rc))


def on_message(mosq, userdata, msg):
    global final_mid
    if msg.retain == 0:
        pass
        #sys.exit()
    else:
        if userdata == True:
            print("Clearing topic "+msg.topic)
        (rc, final_mid) = mosq.publish(msg.topic, None, 1, True)


def on_publish(mosq, userdata, mid):
    global final_mid
    if mid == final_mid:
        sys.exit()


def on_log(mosq, userdata, level, string):
    print(string)


def print_usage():
    print(
        "mqtt_clear_retain.py [-d] [-h hostname] [-i clientid] [-k keepalive] "
        "[-p port] [-u username [-P password]] [-v] -t topic")


def main(argv):
    debug = False
    host = "localhost"
    client_id = None
    keepalive = 60
    port = 1883
    password = None
    topic = None
    username = None
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "dh:i:k:p:P:t:u:v", [
            "debug", "id", "keepalive", "port", "password", "topic",
            "username", "verbose"])
    except getopt.GetoptError as s:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-i", "--id"):
            client_id = arg
        elif opt in ("-k", "--keepalive"):
            keepalive = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-P", "--password"):
            password = arg
        elif opt in ("-t", "--topic"):
            topic = arg
            print(topic)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    if topic == None:
        print("You must provide a topic to clear.")
        sys.exit(2)

    mqttc = paho.Client(client_id)
    mqttc._userdata = verbose
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    if debug:
        mqttc.on_log = on_log

    if username:
        mqttc.username_pw_set(username, password)
    mqttc.connect(host, port, keepalive)
    mqttc.subscribe(topic)
    mqttc.loop_forever()


if __name__ == "__main__":
    main(sys.argv[1:])
