from flask import Flask, request, jsonify, send_file, send_from_directory
import util
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.join(current_dir, '..', 'client')

app = Flask(__name__, static_folder=client_dir, static_url_path='/static')

@app.route('/', methods=['GET'])
def home():
    return send_file(os.path.join(client_dir, 'app.html'))

# Add this route to handle files at the root level
@app.route('/<path:filename>')
def serve_root_static(filename):
    return send_from_directory(client_dir, filename)

# Static files route - serves any files from the client directory
@app.route('/client/<path:path>')
def serve_client_files(path):
    return send_from_directory(client_dir, path)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bath = int(request.form['bath'])
    balcony = int(request.form['balcony'])
    bhk = int(request.form['bhk'])
    
    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bath,balcony,bhk)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()