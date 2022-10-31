import psycopg2

class querying():
    def __init__(self):
        self.connection = psycopg2.connect(database="vaticle", user="mydatabaseuser", password="p", host="localhost", port=5432)

        self.queryCursor = connection.cursor()

    def main():

        while True:
            mode = input("station(s) or line(l)")


            if mode.lower() == "s":

                station = input("input station ")

                sql = "SELECT stationId FROM stations WHERE stationName= %s"

                self.queryCursor.execute(sql, (station, ))

                stationId = self.queryCursor.fetchone()[0]
                

                sql = "SELECT lineId FROM lineStation WHERE stationId= %s"

                self.queryCursor.execute(sql, (stationId, ))

                lineIds = self.queryCursor.fetchall()

                print(f"There are {len(lineIds)} lines")

                sql = "SELECT lineName FROM lines WHERE lineId = %s "
                for lineId in lineIds:
                    self.queryCursor.execute(sql, (lineId, ))

                    line = self.queryCursor.fetchone()
                    
                    print(line[0])


            elif mode.lower() == "l":
                line = input("input line ")

                sql = "SELECT lineId FROM lines WHERE lineName = %s"

                self.queryCursor.execute(sql, (line, ))

                lineId = self.queryCursor.fetchone()[0]

                sql = "SELECT stationId from lineStation WHERE lineId= %s"

                self.queryCursor.execute(sql, (lineId, ))

                stationIds = self.queryCursor.fetchall()

                print(f"There are {len(stationIds)} stations")

                sql = "SELECT stationName from stations WHERE stationId= %s"

                for stationId in stationIds:
                    self.queryCursor.execute(sql, (stationId, ))

                    station = self.queryCursor.fetchone()

                    print(station[0])

                
            elif mode.lower() == "l":
                break
            else:
                print("Invalid input please try again")

