import random
import hashlib
from datetime import datetime, timedelta
from Database import Database
from MongoGetterSetter import MongoGetterSetter

db = Database.get_connection()
users = db.users

class MongoGetterSetter:
    def __init__(self,phone_number):
        self._collection = db.users
        self._filter_query = {
            "$or": [
                {"phone_number": phone_number}, 
                {"id": phone_number}
            ]
            
    def get_user_by_phone(self, phone_number):
        """ Retrieve a user document by phone number. """
        return self.db.users.find_one({"phone_number": phone_number})

    def insert_otp(self, otp_data):
        """ Insert a new OTP document into the database. """
        return self.db.otps.insert_one(otp_data)

    def find_otp(self, user_id, hashed_otp):
        """ Find an OTP document that matches the user ID and hashed OTP. """
        return self.db.otps.find_one({
            "user_id": user_id,
            "otp_code": hashed_otp,
            "expires_at": {"$gte": datetime.now()}
        })

    def delete_otp(self, otp_id):
        """ Delete an OTP document by ID. """
        return self.db.otps.delete_one({"_id": otp_id})
        

    class OTPManager:
    def __init__(self, uri, db_name):
        self.mongo_accessor = MongoGetterSetter(uri, db_name)

    def generate_otp(self, phone_number):
        """ Generate and store OTP for a given phone number """
        user = self.mongo_accessor.get_user_by_phone(phone_number)
        if not user:
            return None  # User not found

        # Generate a random 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        hashed_otp = hashlib.sha256(otp_code.encode()).hexdigest()

        # Setting OTP validity for 5 minutes
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=5)

        # Store OTP in the database
        otp_data = {
            "user_id": user["_id"],
            "otp_code": hashed_otp,
            "created_at": created_at,
            "expires_at": expires_at
        }
        self.mongo_accessor.insert_otp(otp_data)
        
        # Return the plaintext OTP code for sending via SMS
        return otp_code

    def verify_otp(self, phone_number, otp_code):
        """ Verify an OTP code provided by the user """
        user = self.mongo_accessor.get_user_by_phone(phone_number)
        if not user:
            return False

        hashed_otp = hashlib.sha256(otp_code.encode()).hexdigest()
        otp_entry = self.mongo_accessor.find_otp(user["_id"], hashed_otp)

        if otp_entry:
            # Optionally delete the OTP after verification
            self.mongo_accessor.delete_otp(otp_entry["_id"])
            return True
        return False