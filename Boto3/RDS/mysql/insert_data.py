import pymysql

def insert_data():

    try:
        mydb = pymysql.connect(
            host="rdstest.c9rhzfcjvz27.us-east-2.rds.amazonaws.com",
            user="admin",
            password="password",
            database="dbmlruns"
        )

        mycursor = mydb.cursor()

        name = input("Please enter your name : ")
        lastname = input("Please enter your lastname : ")


        query = "INSERT INTO Person (name, lastname) VALUES (%s, %s)"
        value = (name,lastname)

        mycursor.execute(query, value)

        mydb.commit()
        print("Data Inserted")


    except pymysql.MySQLError as e:
        print("Failed to add data {} ".format(e))

if __name__ == '__main__':
    insert_data()