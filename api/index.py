from flask import Flask, request, jsonify, render_template, redirect
from app import generate_Content
from app.services.call_esp8266 import light_control, get_sensor_data, get_status as get_esp_status
import logging
import os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.template_folder = os.path.join(os.path.dirname(__file__), "../templates")
app.static_folder = os.path.join(os.path.dirname(__file__), "../static")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/introduction", methods=["GET"])
def introduction():
    return render_template("introduction.html")

@app.route("/esp_sensor", methods=["GET"])
def esp_sensor():
    sensor = get_sensor_data()
    return jsonify({
        "temperature": sensor.get("temperature"),
        "humidity": sensor.get("humidity"),
        "message": sensor.get("content")
    })

@app.route("/bot", methods=["POST"])
def botController():
    req: dict = request.get_json()
    message = req.get("message", None)
    attchment = req.get('attchment', None)

    response = generate_Content(prompt=message, attchment=attchment) or "Xảy ra lỗi. Tôi là CHATBOT."
    app.logger.info("model message")
    return jsonify({
        "model": response
    }), 200

@app.route("/toggle_led1", methods=["GET", "POST"])
def toggle_led1():
    result = light_control(status="toggle", led="1")
    return jsonify({"message": result["content"]})

@app.route("/toggle_led2", methods=["GET", "POST"])
def toggle_led2():
    result = light_control(status="toggle", led="2")
    return jsonify({"message": result["content"]})

@app.route("/toggle_led3", methods=["GET", "POST"])
def toggle_led3():
    result = light_control(status="toggle", led="3")
    return jsonify({"message": result["content"]})

@app.route("/toggle_led4", methods=["GET", "POST"])
def toggle_led4():
    result = light_control(status="toggle", led="4")
    return jsonify({"message": result["content"]})

@app.route("/get_status", methods=["GET"])
def get_status():
    status = get_esp_status()
    return jsonify(status)

@app.route("/control_all", methods=["GET", "POST"])
def control_all():
    action = request.args.get("action", "off")
    if action not in ["on", "off"]:
        action = "off"
    result = light_control(status=action, led="all")
    return jsonify({"message": result["content"]})


# Vercel expects the Flask app to be named 'app'