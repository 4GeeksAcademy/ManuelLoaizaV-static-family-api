import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import generate_sitemap, validate_payload
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")
jackson_family.add_member(
    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    }
)
jackson_family.add_member(
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    }
)
jackson_family.add_member(
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
)

# See https://flask.palletsprojects.com/en/3.0.x/errorhandling/#returning-api-errors-as-json

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

@app.route("/")
def sitemap():
    return generate_sitemap(app)

@app.route("/members", methods=["GET"])
def fetch_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route("/members/<int:member_id>", methods=["GET"])
def fetch_member(member_id):
    family_member = jackson_family.get_member(member_id)
    if family_member is None:
        raise InvalidAPIUsage(
            message=f"Family member {member_id} not found",
            status_code=404
        )
    return jsonify(family_member), 200

@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    # See https://stackoverflow.com/a/25970628/9041490
    if jackson_family.delete_member(member_id):
        return (""), 200
    return (""), 204

@app.route("/members", methods=["POST"])
def create_member():
    payload = request.get_json()
    is_valid, errors = validate_payload(payload)
    if not is_valid:
        # See https://www.rfc-editor.org/rfc/rfc4918#section-11.2
        raise InvalidAPIUsage(
            message="Unprocessable Entity",
            status_code=422,
            payload=errors
        )
    new_member = jackson_family.add_member(payload)
    return jsonify(new_member), 201

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
