import mysql.connector as mc


def show_tables():
    try:
        mydb = mc.connect(
            host="rdstest.c9rhzfcjvz27.us-east-2.rds.amazonaws.com",
            user="admin",
            password="password",
            database="rdstest"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SHOW TABLES")

        for table in mycursor:
            print(table)


    except mc.Error as e:
        print("Can not show the tables {} ".format(e))

if __name__ == '__main__':
    show_tables()
