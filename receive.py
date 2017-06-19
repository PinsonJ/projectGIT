import serial
import MySQLdb as mdb

arduino = serial.Serial("/dev/ttyUSB0")
arduino.baudrate=9600

data = arduino.readline()
pieces = data.split(":")
temperature = pieces[0]
humidity = pieces[1]
pressure = pieces[2]
rainsensor = pieces[3]


con = mdb.connect('localhost','root', 'test', 'weerstation')

with con:
    cursor = con.cursor()
    cursor.execute("""INSERT INTO weerstation VALUES('',%s,%s,%s,%s,CURRENT_TIMESTAMP )""", (float(temperature),float(humidity),float(pressure),int(rainsensor)))
    con.commit()
    cursor.close()


