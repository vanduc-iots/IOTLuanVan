import base64
from flask import Flask, request, jsonify, render_template, redirect
from app import generate_Content
from app.services.call_esp8266 import light_control, get_sensor_data, get_status as get_esp_status
import logging
import openai
from setup import OPENAI_API_KEY

_app = Flask(__name__)
_app.logger.setLevel(logging.INFO)
_app.template_folder = "templates"
_app.static_folder = "static"

@_app.route("/", methods = ["GET"])
def home():
    return render_template("home.html")

@_app.route("/introduction", methods = ["GET"])
def introduction():
    return render_template("introduction.html")

@_app.route("/esp_sensor", methods=["GET"])
def esp_sensor():
    sensor = get_sensor_data()
    return jsonify({
        "temperature": sensor.get("temperature"),
        "humidity": sensor.get("humidity"),
        "message": sensor.get("content")
    })

@_app.route("/toggle_led1", methods=["GET", "POST"])
def toggle_led1():
    print("Toggle LED1 called")
    result = light_control(status="toggle", led="1")
    print(f"Result: {result}")
    return jsonify({"message": result["content"]})

@_app.route("/toggle_led2", methods=["GET", "POST"])
def toggle_led2():
    print("Toggle LED2 called")
    result = light_control(status="toggle", led="2")
    print(f"Result: {result}")
    return jsonify({"message": result["content"]})

@_app.route("/toggle_led3", methods=["GET", "POST"])
def toggle_led3():
    print("Toggle LED3 called")
    result = light_control(status="toggle", led="3")
    print(f"Result: {result}")
    return jsonify({"message": result["content"]})

@_app.route("/toggle_led4", methods=["GET", "POST"])
def toggle_led4():
    print("Toggle LED4 called")
    result = light_control(status="toggle", led="4")
    print(f"Result: {result}")
    return jsonify({"message": result["content"]})

@_app.route("/get_status", methods=["GET"])
def get_status():
    status = get_esp_status()
    return jsonify(status)

@_app.route("/control_all", methods=["GET", "POST"])
def control_all():
    action = request.args.get("action", "off")
    print(f"Control all called with action: {action}")
    if action not in ["on", "off"]:
        action = "off"
    result = light_control(status=action, led="all")
    print(f"Result: {result}")
    return jsonify({"message": result["content"]})

@_app.route("/tts", methods=["POST"])
def tts_api():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400

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
        _app.logger.exception("TTS generation failed")
        return jsonify({"error": str(e)}), 500


@_app.route("/bot", methods=["POST"])
def botController():
    req: dict = request.get_json()
    message = req.get("message", None)
    attchment = req.get('attchment', None)

    response:str = generate_Content(prompt=message, attchment=attchment) or "Xảy ra lỗi. Tôi là CHATBOT."
    _app.logger.info("model message")
    return jsonify({
        "model": response
    }), 200


if __name__ == "__main__":
    _app.run(host="0.0.0.0", port=8080, debug=True)
    