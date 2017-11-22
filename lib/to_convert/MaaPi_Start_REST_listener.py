from bottle import route, run
import psycopg2
from MaaPi_Settings import Maapi_rest_server_port
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def stringToList(self):
    command_list=[]
    command_text=""
    for i in self:
        if i.isspace():
            command_list.append(command_text)
            command_text=""
            continue
        command_text+=i
    command_list.append(command_text)
    return command_list

@route('/put/<name>', method='PUT')
def recipe_save( name="Mystery Recipe"):
    dd=name.decode("hex")
    list_put=stringToList(dd)
    sysname=list_put[1]
    devId=list_put[3]
    state=int(list_put[5])+0
    gpioPin=int(list_put[7])+0
    GPIO.setwarnings(False)
    GPIO.setup(gpioPin, GPIO.OUT)
    rs=GPIO.input(gpioPin)
    GPIO.output(gpioPin,state)

    #SysName dupa DevId 2142 state 1 gpioPin 4
    #5379734e616d65206475706120446576496420323134322073746174652031206770696f50696e2034


    return "gpio {0} state {1} real state: {2}\n".format(gpioPin,state,rs)


run(host='0.0.0.0', port=Maapi_rest_server_port, debug=True)
