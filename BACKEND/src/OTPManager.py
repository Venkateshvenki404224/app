import random
import hashlib
from datetime import datetime, timedelta
from src.Database import Database
from mongogettersetter import MongoGetterSetter
from src.User import Users

db = Database.get_connection()
otp = db.otp

class OTPManagerCollection(metaclass=MongoGetterSetter):
    def __init__(self,phone_number):
        self._collection = db.otp
        self._filter_query = {"phone_number": phone_number}


class OTPManager:
    def __init__(self,phone_number):
        self._collection = OTPManagerCollection(phone_number)
        self.phone_number = phone_number

         # Create a new document if it doesn't exist
        if self._collection.get() is None:
            self._collection.insert_one(self._filter_query)   

    @staticmethod
    def generate_otp(phone_number):
        """ Generate and store OTP for a given phone number """
        user = otp.find_one({"phone_number": phone_number
        })
        if user:
            # Generate a random 6-digit OTP
            otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            hashed_otp = hashlib.sha256(otp_code.encode()).hexdigest()

            # Setting OTP validity for 5 minutes
            created_at = datetime.now()
            expires_at = created_at + timedelta(minutes=5)

            # Store OTP in the database
            otp_data = {
                "phone_number": phone_number,
                "otp_code": hashed_otp,
                "otp": otp_code,
                "created_at": created_at,
                "expires_at": expires_at
            }
            result = otp.insert_one(otp_data)
            if result:
                return {
                    "status": 200,
                    "otp": otp_code
                }
            else:
                return {
                    "status": 400,
                    "message": "Failed to generate OTP"
                }
        else:
            return {
                "status": 400,
                "message": "User not found"
            }

    def delete_otp(phone_number):
        """ Delete the OTP document for a given phone number """
        result = otp.delete_one({"phone_number": phone_number})
        if result.deleted_count > 0:
            return {
                "status": 200,
                "message": "OTP document deleted successfully"
            }
        else:
            return {
                "status": 400,
                "message": "Failed to delete OTP document"
            }

    def verify_otp(phone_number, otp_code):
        """ Verify an OTP code provided by the user, checking its time validity. """
        # Attempt to find the user and the associated OTP data based on phone number
        user_otp_data = otp.find_one({"phone_number": phone_number})

        print(user_otp_data)  # Debug print to see what data is being fetched

        if not user_otp_data:
            return {
                "status": 401,
                "message": "There is no user with this phone number"
            }

        # Check if the provided OTP matches the stored OTP and is within the validity period
        if user_otp_data.get("otp") == otp_code:
            # Check the current time against the expires_at field
            current_time = datetime.now()
            expires_at = user_otp_data.get("expires_at")
            print(current_time, expires_at)  # Debug print to see the current time and expiry time
            if expires_at and current_time <= expires_at:
                # Delete the OTP document after successful verification
                OTPManager.delete_otp(phone_number)
                return {
                    "status": 200,
                    "message": "OTP verified successfully"
                }
            else:
                return {
                    "status": 401,
                    "message": "OTP has expired"
                }
        else:
            return {
                "status": 400,
                "message": "Invalid OTP"
            }