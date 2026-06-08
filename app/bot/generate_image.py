import openai
from PIL import Image
from io import BytesIO
from setup import OPENAI_API_KEY
import base64, mimetypes

def generateImage(prompt, attchment=None, retries=0):
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        result = {"content": "Image generated successfully", 'image': []}
        for data in response.data:
            image_url = data.url
            # Download image
            import requests
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            result['image'].append(img)
        return result
    except Exception as e:
        print("Lỗi tạo ảnh OpenAI: ", e)
        if retries < 2:
            return generateImage(prompt, attchment, retries + 1)
        return {"content": "Lỗi tạo ảnh", 'image': []}

if __name__ == "__main__" :
    generateImage('tạo ảnh cận cảnh một người phụ nữ ở độ tuổi 20, ảnh đường phố, ảnh tĩnh trong phim, tông màu cam ấm dịu')