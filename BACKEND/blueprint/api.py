from flask import Blueprint, render_template, request,jsonify
from src.Database import Database
from geopy.distance import geodesic
from src import get_config , generate_otp
from src.OTPManager import OTPManager

bp = Blueprint("api", __name__, url_prefix="/")
db = Database.get_connection()



@bp.route("/", methods=["GET"])
def home():
    api_key = get_config("GOOGLE_MAPS_API_KEY")
    return render_template("index.html", api_key=api_key)

@bp.route('/calculate_distance', methods=['GET', 'POST'])
def calculate_distance():
    distance = None  # Default to not showing any distance
    if request.method == 'POST':
        # Extract form data
        pickup_lat = request.form.get('pickup_lat')
        pickup_lng = request.form.get('pickup_lng')
        dropoff_lat = request.form.get('dropoff_lat')
        dropoff_lng = request.form.get('dropoff_lng')
        api_key = get_config("GOOGLE_MAPS_API_KEY")

        if pickup_lat and pickup_lng and dropoff_lat and dropoff_lng:
            # Calculate distance
            pickup_location = (pickup_lat, pickup_lng)
            dropoff_location = (dropoff_lat, dropoff_lng)
            distance = geodesic(pickup_location, dropoff_location).kilometers
            distance = f"{distance:.2f} km"  # Format distance

    # Render the same template whether it's a GET or POST request
    return render_template("index.html", distance=distance, api_key=api_key)



@bp.route('/generate_otp', methods=['POST'])
def generate_otp():
    phone_number = request.form.get('phone_number')
    print(phone_number)
    if phone_number:
        result = OTPManager.generate_otp(phone_number)
        print(result)
        if result["status"] == 200:
           return{
                "status": 200,
                "message": "OTP generated successfully",
                "otp_code": result['otp']
           }
        else:
            return {
                "status": 400,
                "message": "Failed to generate OTP"
            }
    else:
        return {
            "status": 400,
            "message": "Invalid phone number"
        }


@bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone_number = request.form.get('phone_number')
    otp_code = request.form.get('otp_code')
    if phone_number and otp_code:
        result = OTPManager.verify_otp(phone_number, otp_code)
        print(result)
        if result["status"] == 200:
            return {
                "status": 200,
                "message": "OTP verified successfully"
            }
        else:
            return {
                "status": result["status"],
                "message": result["message"]
            }
    else:
        return {
            "status": 400,
            "message": "Invalid phone number or OTP"
        }