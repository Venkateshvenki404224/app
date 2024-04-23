from flask import Blueprint, render_template, request,jsonify
from src.Database import Database
from geopy.distance import geodesic
from src import get_config , generate_otp

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



    @bp.route('/check_phone_number', methods=['POST'])
    def check_phone_number():
        phone_number = request.form.get('phone_number')
        if phone_number:
            # Check if phone number exists in the database
            if db.check_phone_number(phone_number):
                # Generate a random number
                random_number = generate_otp()
                # Store the random number in the database
                db.store_random_number(phone_number, random_number)
                return jsonify({'message': 'Random number generated and stored successfully'})
            else:
                return jsonify({'error': 'Phone number does not exist in the database'}), 400
        else:
            return jsonify({'error': 'Phone number is missing'}), 400
