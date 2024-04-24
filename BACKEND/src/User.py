from src.Database import Database
from mongogettersetter import MongoGetterSetter


db = Database.get_connection()
users = db.users  # This collection will store both agents and Telegram users

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self, phone_number):
        self._collection = db.users
        self._filter_query = {"phone_number": phone_number}

class Users:
        def __init__(self, id):
            self.collection = UserCollection(id)
            self.id = self.collection.id
            self.phone_number = self.collection.phone_number

        @staticmethod
        def create_driver(self, first_name, last_name, address, phone_number, vehicle_type, license_number, dob, vehicle_number):
            try:
                user = {
                    "first_name": name,
                    "last_name": "",
                    "permanent_address": "",
                    "phone_number": phone_number,
                    "vehicle_type": vehicle_type,
                    "license_number": "",
                    "dob": "",
                    "vehicle_number": vehicle_number,
                    "is_driver": True,
                    "is_active": False,
                }
                self.collection.insert_one(user)
                return {
                    "status": 200,
                    "message": "Driver created successfully"
                }
            except Exception as e:
                return {
                    "status": 400,
                    "message": str(e)
                }   

        @staticmethod
        def create_user(self, first_name, last_name, address, phone_number):
            try:
                user = {
                    "first_name": name,
                    "last_name": "",
                    "permanent_address": "",
                    "phone_number": phone_number,
                    "is_driver": False,
                    "is_active": False,
                }
                self.collection.insert_one(user)
                return {
                    "status": 200,
                    "message": "User created successfully"
                }
            except Exception as e:
                return {
                    "status": 400,
                    "message": str(e)
                }

        @staticmethod
        def check_number(phone_number):
            result = db.find_one({'phone_number': phone_number})
            if result:
                return {
                    "name": result['name'],
                    "status": 200
                }  
            else:
                return {
                    "error": "Number does not exist",
                    "status": 400
                }


    
