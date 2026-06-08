import requests
import time
import os

ESP8266_HOST = os.getenv("ESP8266_HOST", "10.206.193.211")

REQUEST_TIMEOUT = (2, 3)
MAX_RETRY = 3

session = requests.Session()


def call_esp(url):

    try:
        headers = {
            "Connection": "close"
        }

        return session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers=headers
        )

    except requests.exceptions.Timeout:
        return "TIMEOUT"

    except requests.exceptions.ConnectionError:
        return "CONN_ERROR"

    except Exception as e:
        return str(e)

def light_control(status=None, led="all"):

    if not status:
        return {
            "content": "Không có lệnh điều khiển mới.",
            "image": []
        }

    status = str(status).lower().strip()
    led = str(led).lower().strip()

    if status not in ["on", "off", "toggle"]:
        return {
            "content": f"Lệnh không hợp lệ: {status}",
            "image": []
        }

    valid_leds = ["1", "2", "3", "4"]
    if led not in valid_leds and led != "all":
        led = "all"

    leds = valid_leds if led == "all" else [led]

    result = {}

    for l in leds:
        url = f"http://{ESP8266_HOST}/led{l}/{status}"
        response = call_esp(url)

        if isinstance(response, str):
            return {
                "content": f"Lỗi ESP: {response}",
                "image": []
            }

        result[l] = "OK"

    return {
        "content": f"Đã {status} LED {led}",
        "image": []
    }


def get_status():
    url = f"http://{ESP8266_HOST}/status"

    for attempt in range(MAX_RETRY):
        response = call_esp(url)

        if isinstance(response, str):
            time.sleep(0.5)
            continue

        if response.status_code != 200:
            time.sleep(0.5)
            continue

        try:
            return response.json()
        except Exception as e:
            return {
                "led1": "UNKNOWN",
                "led2": "UNKNOWN",
                "led3": "UNKNOWN",
                "led4": "UNKNOWN",
                "error": str(e)
            }

    return {
        "led1": "UNKNOWN",
        "led2": "UNKNOWN",
        "led3": "UNKNOWN",
        "led4": "UNKNOWN"
    }


def get_sensor_data():

    url = f"http://{ESP8266_HOST}/sensor"

    for attempt in range(MAX_RETRY):

        response = call_esp(url)

        if isinstance(response, str):
            time.sleep(0.5)
            continue

        if response.status_code != 200:
            time.sleep(0.5)
            continue

        try:

            data = response.json()

            return {
                "content": (
                    f"Nhiệt độ: {data['temperature']}°C\n"
                    f"Độ ẩm: {data['humidity']}%"
                ),
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "image": []
            }

        except Exception as e:
            return {
                "content": f"Lỗi parse JSON: {e}",
                "image": []
            }

    return {
        "content": "Không đọc được dữ liệu DHT11",
        "image": []
    }