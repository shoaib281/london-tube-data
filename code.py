import psycopg2
import json


connection = psycopg2.connect(database="vaticle", user="mydatabaseuser", password="p", host="localhost", port=5432)

cursor = connection.cursor()

cursor.execute("CREATE TABLE stations (stationId VARCHAR(255) PRIMARY KEY, stationName VARCHAR(255), longitude decimal, latitude decimal)")

cursor.execute("CREATE TABLE lines (lineId SERIAL PRIMARY KEY, lineName VARCHAR(255))")

cursor.execute("CREATE TABLE lineStation (lineStationId SERIAL PRIMARY KEY, stationId VARCHAR(255) REFERENCES stations, lineId SERIAL REFERENCES lines)")

cursor.close()

with open("train-network.json") as file:
    data  = json.load(file)

    stations = data["stations"]
    lines = data["lines"]

    stationCursor = connection.cursor()

    sql = "INSERT INTO stations (stationId, stationName, longitude, latitude) VALUES (%s, %s, %s, %s)"

    for station in stations:
        stationCursor.execute(sql, (station["id"], station["name"], station["longitude"], station["latitude"], ))

    stationCursor.close()

    lineCursor = connection.cursor()
        
    sql = "INSERT INTO lines (lineName) VALUES (%s) RETURNING lineId"
    sql2 = "INSERT INTO lineStation (stationId, lineId) VALUES (%s, %s)"

    for line in lines:
       lineCursor.execute(sql, (line["name"], )) 
       lineId = lineCursor.fetchone()[0]

       for station in line["stations"]:
           lineCursor.execute(sql2, (station, lineId, ))

    lineCursor.close()

queryCursor = connection.cursor()

while True:
    mode = input("station(s) or line(l)")


    if mode.lower() == "s":

        station = input("input station ")

        sql = "SELECT stationId FROM stations WHERE stationName= %s"

        queryCursor.execute(sql, (station, ))

        stationId = queryCursor.fetchone()[0]
        

        sql = "SELECT lineId FROM lineStation WHERE stationId= %s"

        queryCursor.execute(sql, (stationId, ))

        lineIds = queryCursor.fetchall()

        print(f"There are {len(lineIds)} lines")

        sql = "SELECT lineName FROM lines WHERE lineId = %s "
        for lineId in lineIds:
            queryCursor.execute(sql, (lineId, ))

            line = queryCursor.fetchone()
            
            print(line[0])


    elif mode.lower() == "l":
        line = input("input line ")

        sql = "SELECT lineId FROM lines WHERE lineName = %s"

        queryCursor.execute(sql, (line, ))

        lineId = queryCursor.fetchone()[0]

        sql = "SELECT stationId from lineStation WHERE lineId= %s"

        queryCursor.execute(sql, (lineId, ))

        stationIds = queryCursor.fetchall()

        print(f"There are {len(stationIds)} stations")

        sql = "SELECT stationName from stations WHERE stationId= %s"

        for stationId in stationIds:
            queryCursor.execute(sql, (stationId, ))

            station = queryCursor.fetchone()

            print(station[0])

        
    elif mode.lower() == "l":
        break
    else:
        print("Invalid input please try again")

