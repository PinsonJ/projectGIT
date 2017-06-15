import serial
import MySQLdb as mdb

arduino = serial.Serial("/dev/ttyUSB0")
arduino.baudrate=9600

data = arduino.readline()
pieces = data.split(":")
temperature = pieces[0]
humidity = pieces[1]
pressure = pieces[2]
rainsensor = pieces[4]
light = pieces[3]

con = mdb.connect('localhost','root', '', 'weerstation')

with con:
    # mysql.WriteData(temperature,humidity,pressure,rainsensor,light)
    cursor = con.cursor()
    cursor.execute("""INSERT INTO weerstation VALUES('',%s,%s,%s,%s,%s,CURRENT_TIMESTAMP )""", (float(temperature),float(humidity),int(pressure),int(rainsensor),int(light)))
    con.commit()
    cursor.close()


