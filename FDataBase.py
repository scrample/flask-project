import sqlite3
import time
import math
import math
import re
from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Error read form database')
        return []


    def addUser(self, email, hashPassword):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('SOMEONE ELSE HAVE YOUR NAME')
                return False

            tm = math.floor(time.time())
            rank = 'visitor'
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?,?,?,?)",(email,hashPassword,tm,rank))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT USER IN DB" + str(e))
            return False
            
        return True


    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not defind")
                return False

            return res

        except sqlite3.Error as e:
            print("ERROR GET DATA FROM DATABASE" + str(e))

        return False


    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not defind")
                return False

            return res

        except sqlite3.Error as e:
            print("ERRER GET DATA FROM DATABASE"+str(e))

        return False


    #add employee by admin
    def addEmployee(self, email, hashPassword):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('SOMEONE ELSE HAVE YOUR NAME')
                return False

            tm = math.floor(time.time())
            rank = 'employee'
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?,?,?,?)",(email,hashPassword,tm,rank))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT USER IN DB" + str(e))
            return False
            
        return True


    #Add car by admin
    def AddCarByAdmin(self, model, car_nubmer, price):
        try:
            self.__cur.execute("INSERT INTO cars VALUES(NULL, ?,?,?)",(model,car_nubmer,price))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT CAR IN DB" + str(e))
            return False
            
        return True


    #Add client by employee
    def AddClientByEmployee(self, name, surname, phone, employeeid):
        try:
            self.__cur.execute("INSERT INTO clients VALUES(NULL, ?,?,?,?)",(name,surname,phone,employeeid))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT CLIENT IN DB" + str(e))
            return False
            
        return True

    #Add fines to client by employee
    def AddFinesToClient(self, ClientID, Reason, Finesum, employeeid):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO fines VALUES(NULL, ?,?,?,?,?)",(ClientID,tm,Reason,Finesum,employeeid))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT FINES IN DB" + str(e))
            return False
            
        return True

    #Add reservation by employee
    def AddReservation(self, clientID, carID, time, employeeid):
        try:
            self.__cur.execute("INSERT INTO reservation VALUES(NULL, ?,?,?,?)",(clientID,carID,time,employeeid))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT RESERVATION IN DB" + str(e))
            return False
            
        return True


    def getClientIDbyNameAndSurname(self, name, surname):
        try:
            self.__cur.execute(f"SELECT client_id FROM clients WHERE name = '{name}' AND surname = '{surname}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not defind")
                return False
            return res

        except sqlite3.Error as e:
            print("ERROR GET DATA FROM DATABASE" + str(e))

        return False

    
    def getPriceByCarID(self, carID):
        try:
            self.__cur.execute(f"SELECT price FROM cars WHERE car_id = '{carID}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not defind")
                return False
            return res

        except sqlite3.Error as e:
            print("ERROR GET DATA FROM DATABASE" + str(e))

        return False


    def getCarIDByModel(self, carModel):
        try:
            self.__cur.execute(f"SELECT car_id FROM cars WHERE model = '{carModel}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not defind")
                return False
            return res

        except sqlite3.Error as e:
            print("ERROR GET DATA FROM DATABASE" + str(e))

        return False

    
    #Add reservation by employee
    def AddRecord(self, clientID, carID, employeeid, recordsum):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO record VALUES(NULL, ?,?,?,?,?)",(clientID,carID,tm,employeeid, recordsum))    
            self.__db.commit()

        except sqlite3.Error as e:
            print("CANNOT INSERT RECORD IN DB" + str(e))
            return False
            
        return True


    def GetAllClients(self):
        sql = '''SELECT client_id, name, surname,phone_number FROM clients'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Error read form database')
        return []


    def GetAllCars(self):
        sql = '''SELECT car_id, model, car_number,price FROM cars'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Error read form database')
        return []