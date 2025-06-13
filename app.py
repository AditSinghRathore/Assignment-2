from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from cloudant.client import Cloudant
from cloudant.error import CloudantException

app = Flask(__name__)
CORS(app)

# Cloudant credentials
apikey = "QR_qjOTj8Jfsn2Y02cShVI7EL9cJ9tpuAJnp1npZi8Fj"
url = "https://55517355-960c-4aca-b390-67df816e10e6-bluemix.cloudantnosqldb.appdomain.cloud"
username = "55517355-960c-4aca-b390-67df816e10e6-bluemix"
db_name = "db_server"

# Connect to Cloudant
client = Cloudant.iam(username, apikey, url=url, connect=True)
try:
    db = client[db_name]
except CloudantException:
    db = client.create_database(db_name)

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/create', methods=['POST'])
@app.route('/create', methods=['POST'])
def create_record():
    try:
        data = request.get_json()
        print("Received:", data)

        name = data.get('name')
        email = data.get('email')
        feedback = data.get('feedback')

        if not name or not email or not feedback:
            return jsonify({"error": "Missing name, email, or feedback"}), 400

        document = {
            "name": name,
            "email": email,
            "feedback": feedback
        }
        db.create_document(document)
        print("Saved document:", document)

        return jsonify({"message": "Record created successfully!"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/get_records', methods=['GET'])
def get_records():
    try:
        records = []
        for document in db:
            records.append({
                "name": document.get("name"),
                "email": document.get("email"),
                "feedback": document.get("feedback")
            })
        return jsonify(records)
    except Exception as e:
        print("Error in /get_records:", e)
        return jsonify({"error": "Internal Server Error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
