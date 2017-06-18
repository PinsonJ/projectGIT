class DbClass:
    def __init__(self):
        import mysql.connector as connector
        # import MySQLdb as mdb

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "test",
            "db": "weerstation"
        }

        self.__connection = connector.connect(**self.__dsn)


    def createUser(self,username, password):
        # sqlQuery2 = ("insert into users(Username,Password) values ('{param1},{param2}')")
        # sqlCommand2 = sqlQuery2.format(param1=username,param2=password)
        # self.__cursor.execute(sqlCommand2)
        cursor = self.__connection.cursor()
        cursor.callproc('sp_createUser',(username,password))
        # print(result)

        self.__connection.commit()
        cursor.close()

    def checkUser(self,username,password):
        sqlQuery = "SELECT * FROM users WHERE Username ='"+username+"' and Password = '"+password+"'"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        user = cursor.fetchone()
        cursor.close()
        return user

    def getLatestTemperature(self):
        # Query zonder parameters
        sqlQuery = "SELECT Temperature FROM weerstation ORDER BY ID DESC LIMIT 1"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        temperature=result
        temperature = str(temperature).split(',')
        temperature = temperature[0]
        temperature = temperature[2:]
        cursor.close()
        return temperature

    def getLatestHumidity(self):
        # Query zonder parameters
        sqlQuery = "SELECT Humidity FROM weerstation ORDER BY ID DESC LIMIT 1"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        humidity=result
        humidity = str(humidity).split(',')
        humidity = humidity[0]
        humidity = humidity[2:]
        cursor.close()
        return humidity

    def getLatestPressure(self):
        # Query zonder parameters
        sqlQuery = "SELECT Pressure FROM weerstation ORDER BY ID DESC LIMIT 1"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        pressure=result
        pressure = str(pressure).split(',')
        pressure = pressure[0]
        pressure = pressure[2:]
        cursor.close()
        return pressure

    def getLatestRainsensor(self):
        # Query zonder parameters
        sqlQuery = "SELECT Rainsensor FROM weerstation ORDER BY ID DESC LIMIT 1"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        rain = result
        rain = str(rain).split(',')
        rain = rain[0]
        rain = rain[2:]
        if int(rain) == 0:
            rain = "Regen"
        elif int(rain) == 1:
            rain = "Lichte regen"
        elif int(rain) == 2:
            rain = "Geen regen"
        cursor.close()
        return rain

    def getLatestLight(self):
        # Query zonder parameters
        sqlQuery = "SELECT light FROM weerstation ORDER BY ID DESC LIMIT 1"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        light=result
        light = str(light).split(',')
        light = light[0]
        light = light[2:]

        cursor.close()
        return light

    def getLatestTimestamp(self):
        # Query zonder parameters
        sqlQuery = "SELECT Timestamp FROM weerstation ORDER BY ID DESC LIMIT 1"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        timestamp = result
        timestamp = str(timestamp).split('(')
        timestamp = timestamp[2]
        timestamp = timestamp.split(')')
        timestamp = timestamp[0]
        timestamp = timestamp.split(',')
        if len(timestamp[1]) ==2:
            month = "0" + (timestamp[1])[1:]
        else:
            month = (timestamp[1])[1:]
        if len(timestamp[4])==2:
            minute = '0' + (timestamp[4])[1:]
        else:
            minute = (timestamp[4])[1:]

        timestamp = timestamp[2] + "-" + month + "-" + timestamp[0] + " " + timestamp[3] + ":" + minute

        cursor.close()
        return timestamp

    def getLast60tempdata(self):
        # Query zonder parameters
        sqlQuery = "SELECT Temperature FROM (SELECT @row := @row +1 AS ID, Temperature FROM (SELECT @row :=0) r, weerstation) ranked WHERE ID % 5 = 0 ORDER BY ID DESC LIMIT 12"
        self.__connection.reset_session()
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        temperature=result
        temperature=str(temperature).replace('(','')
        temperature = str(temperature).replace(')', '')
        temperature = str(temperature).replace(',', '')
        temperature = str(temperature).replace(' ', ',')
        temperature = str(temperature).replace('[', '')
        temperature = str(temperature).replace(']', '')
        temperature = str(temperature).split(',')
        temperature = temperature[11],temperature[10],temperature[9],temperature[8],temperature[7],temperature[6],temperature[5],temperature[4],temperature[3],temperature[2],temperature[1],temperature[0]

        cursor.close()
        return temperature

    def getLast60timedata(self):
        # Query zonder parameters
        sqlQuery = "SELECT Timestamp FROM (SELECT @row := @row +1 AS ID, Timestamp FROM (SELECT @row :=0) r, weerstation) ranked WHERE ID % 5 = 0 ORDER BY ID DESC LIMIT 12"
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        timestamp = result
        timestamp = str(timestamp).split(',')
        timestamp = timestamp[80]+ timestamp[81], timestamp[73]+ timestamp[74], timestamp[66]+ timestamp[67], timestamp[59]+ timestamp[60], timestamp[52]+ timestamp[53], timestamp[45]+ timestamp[46], timestamp[38]+ timestamp[39], timestamp[31]+ timestamp[32], timestamp[24]+ timestamp[25], timestamp[17]+ timestamp[18], timestamp[10]+ timestamp[11],timestamp[3]+ timestamp[4]
        timestamp = str(timestamp).replace("' ", "'")
        timestamp = str(timestamp).replace("(", "")
        timestamp = str(timestamp).replace(")", "")
        timestamp = str(timestamp).replace("'", "")
        timestamp = str(timestamp).replace(", ", ",")
        timestamp = str(timestamp).replace(" ", ":")
        timestamp = str(timestamp).split(',')

        cursor.close()
        return timestamp

    def getLast60humdata(self):
        # Query zonder parameters
        sqlQuery = 'SELECT Humidity FROM (SELECT @row := @row +1 AS ID, Humidity FROM (SELECT @row :=0) r, weerstation) ranked WHERE ID % 5 = 0 ORDER BY ID DESC LIMIT 12'
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        humidity=result
        humidity=str(humidity).replace('(','')
        humidity = str(humidity).replace(')', '')
        humidity = str(humidity).replace(',', '')
        humidity = str(humidity).replace(' ', ',')
        humidity = str(humidity).replace('[', '')
        humidity = str(humidity).replace(']', '')
        humidity = str(humidity).split(',')

        cursor.close()
        return humidity

    def getLast60presdata(self):
        # Query zonder parameters
        sqlQuery = 'SELECT Pressure FROM (SELECT @row := @row +1 AS ID, Pressure FROM (SELECT @row :=0) r, weerstation) ranked WHERE ID % 5 = 0 ORDER BY ID DESC LIMIT 12'
        cursor = self.__connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        pressure=result
        pressure=str(pressure).replace('(','')
        pressure = str(pressure).replace(')', '')
        pressure = str(pressure).replace(',', '')
        pressure = str(pressure).replace(' ', ',')
        pressure = str(pressure).replace('[', '')
        pressure = str(pressure).replace(']', '')
        pressure = str(pressure).split(',')

        cursor.close()
        return pressure




