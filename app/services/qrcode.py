import requests, random
from io import BytesIO
from setup import QR_CODE_API_KEYS

def readQRCode():
    pass


def createQrCode(data, reties=0):
    try:
        prompts = [
            "landscape, oil on matte canvas, sharp details, the expanse scifi spacescape ceres colony, intricate, highly detailed, digital painting, rich color, smooth, sharp focus, illustration, spaceship landed, Unreal Engine 5, 8K, art by artgerm and greg rutkowski and alphonse mucha",
            "a beautiful 3D render of a lotus flower with a bright internal glow, unreal engine 5, cinematic lighting, highly detailed",
            "technology, modern, 3D"
        ]
        payload = {
            "qr_code_data": data,
            "text_prompt": random.choice(prompts),
        }

        response = requests.post(
            "https://api.gooey.ai/v2/art-qr-code",
            headers={
                "Authorization": "bearer " + QR_CODE_API_KEYS[reties],
            },
            json=payload,
        )
        assert response.ok, response.content
        
        from ..bot import generate_Content
        if response.ok: 
            result = response.json()
            model_content = generate_Content("Cho tôi 1 câu phản hồi đã hoàn thành việc tạo mã QR. Kiểu tự nhiên và thông thái")["message"]
            image = result['output']['output_images'][0]
            
        else:
            model_content = generate_Content(f"Cho tôi 1 câu phản hồi bị lỗi bên phía hệ thống của chúng ta")["message"]
            image = ""

        return {
            'content': model_content,
            'image': image
        }
            
    except Exception as e:
        if reties == len(QR_CODE_API_KEYS) -1:
            from logging import error
            error(e)
            return {
                'content': "Có lỗi xảy ra phía chúng tôi",
                'image': ""
            }
        return createQrCode(data=data, reties=reties+1)
        


if __name__ == "__main__":
    pass

