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
    sql2 = "INSERT INTO lineStation (stationId, lineId) (%s, %s)"

    for line in lines:
       lineCursor.execute(sql, (line["name"], )) 
       lineId = lineCursor.fetchone()[0]

       for station in line["stations"]:
           print(lineId, station)
           lineCursor.execute(sql, (lineId, station, ))

    lineCursor.close()
