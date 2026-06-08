import base64
import os
from flask import Flask, request, jsonify, render_template, redirect
from app import generate_Content
from app.services.call_esp8266 import light_control, get_sensor_data, get_status as get_esp_status
import logging
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_SERVER_TTS = os.getenv('USE_SERVER_TTS', 'false').lower() in ('true', '1', 'yes')

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.template_folder = os.path.join(os.path.dirname(__file__), "../templates")
app.static_folder = os.path.join(os.path.dirname(__file__), "../static")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", use_server_tts=USE_SERVER_TTS)

@app.route("/introduction", methods=["GET"])
def introduction():
    return render_template("introduction.html", use_server_tts=USE_SERVER_TTS)

@app.route("/esp_sensor", methods=["GET"])
def esp_sensor():
    sensor = get_sensor_data()
    return jsonify({
        "temperature": sensor.get("temperature"),
        "humidity": sensor.get("humidity"),
        "message": sensor.get("content")
    })

@app.route("/tts", methods=["POST"])
def ttsController():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400

    if not USE_SERVER_TTS:
        return jsonify({"error": "Server-side TTS is disabled"}), 403

    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY is not set"}), 500

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            response_format="mp3",
            input=text
        )
        audio_bytes = response
        if hasattr(response, 'read'):
            audio_bytes = response.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return jsonify({"audio": audio_base64})
    except Exception as e:
        app.logger.exception("TTS generation failed")
        return jsonify({"error": str(e)}), 500

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