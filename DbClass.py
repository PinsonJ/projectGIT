

class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "root",
            "passwd": "",
            "db": "weerstation"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # self.cursor = self.__connection.cursor()

    def getDataFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM tablename"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        # Query met parameters
        sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=voorwaarde)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDatabase(self, value1):
        # Query met parameters
        sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=value1)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    # voor lezen (SELECT)
    # met query(..., return_dict=True) krijg je een dictionary terug,
    # dat vermindert de kans op fouten (zeker bij SELECT * FROM..)
    def query(self, query: str, data: dict = None, dictionary=False):
        cursor = self.__connection.cursor(dictionary=dictionary)
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        return result

        # voor schrijven (INSERT, UPDATE, ...)

    def execute(self, query: str, data: dict = None):
        cursor = self.__connection.cursor()
        cursor.execute(query, data)
        result = cursor.lastrowid
        self.__connection.commit()
        cursor.close()
        return result


    def createUser(self,username, password):
        # sqlQuery2 = ("insert into users(Username,Password) values ('{param1},{param2}')")
        # sqlCommand2 = sqlQuery2.format(param1=username,param2=password)
        # self.__cursor.execute(sqlCommand2)
        self.__cursor.callproc('sp_createUser',(username,password))
        # print(result)

        self.__connection.commit()
        # self.__cursor.close()

    def checkUser(self,username):
        sqlQuery = "SELECT Username FROM users WHERE Username ='"+username+"'"
        self.__cursor.execute(sqlQuery)
        user = self.__cursor.fetchone()
        return user

    def checkPassword(self, username, password):
        sqlQuery = "SELECT Username FROM users WHERE Password ='"+password+"'"


    def WriteData(self,temperature,humidity,pressure,rainsensor,light):
        # Query met parameters
        sqlQuery = "INSERT INTO weerstation VALUES ('','"+temperature+"', '"+humidity+"', '"+pressure+"', '"+rainsensor+"', '"+light+"')"

        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()







