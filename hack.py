from flask import Flask, request, jsonify
import json
import base64
import hashlib
import hmac

app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('config.py')

# Secret key for encoding and decoding HackWebTokens
SECRET_KEY = app.config['SECRET_KEY']


# Encode data
def encode(user, data, context={}):
    header = {"alg": "HS256", "typ": "JWT"}
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()

    payload = {"user": user, "data": data, "context": context}
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

    signature = hmac.new(SECRET_KEY.encode(), f"{header_encoded}.{payload_encoded}".encode(), hashlib.sha256)
    signature_encoded = base64.urlsafe_b64encode(signature.digest()).decode()

    token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    return token


# Decode data
def decode(token, context={}):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    header_encoded, payload_encoded, signature_encoded = parts

    signature = base64.urlsafe_b64decode(signature_encoded)
    expected_signature = hmac.new(SECRET_KEY.encode(), f"{header_encoded}.{payload_encoded}".encode(), hashlib.sha256).digest()

    if signature != expected_signature:
        raise ValueError("Invalid signature")

    payload = json.loads(base64.urlsafe_b64decode(payload_encoded).decode())

    if "context" in payload:
        context.update(payload["context"])

    return {"user": payload["user"], "data": payload["data"]}


@app.route('/encode', methods=['POST'])
def encode_endpoint():
    try:
        request_data = request.get_json()
        user = request_data["user"]
        data = request_data["data"]
        context = request_data.get("context", {})

        encoded_token = encode(user, data, context)

        response_data = {
            "token": encoded_token,
            "context": context
        }

        return jsonify(response_data), 200
    except Exception as e:
        return str(e), 400


@app.route('/decode', methods=['POST'])
def decode_endpoint():
    try:
        request_data = request.get_json()
        token = request_data["token"]
        context = request_data.get("context", {})

        decoded_data = decode(token, context)

        return jsonify(decoded_data), 200
    except Exception as e:
        return str(e), 400


if __name__ == "__main__":
    app.run()
