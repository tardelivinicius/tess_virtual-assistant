import mysql.connector

class Database:

    def __init__(self):
        # Inicia a conexão
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="030595",
            database="virtual_assistant"
            )
        self.mysql = self.connection.cursor()


    def find_access_token(self, access_token):
        self.mysql.execute("SELECT * FROM access_token WHERE access_token LIKE '%{0}%'".format(access_token))
        result = self.mysql.fetchall()
        if len(result) > 0:
            for x in result:
                return x
        else:
            return False

