import base64, os, logging
import openai
from .declaration_funcs import get_func_declaration_tool
from .function_handler import *
from setup import OPENAI_API_KEY


#retries = len(GEMINI_KEYS)-1
def generate_Content(prompt:str, attchment=None) -> dict:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    model = "gpt-4o-mini"  # Use GPT-4o-mini for multimodal support

    messages = [
        {"role": "system", "content": """Nếu có ai hỏi bạn "ai đã sáng tạo ra bạn?" hoặc câu hỏi tương tự thì bạn hãy trả lời người sáng tạo ra bạn là: 
                - Nguyễn Hoàng Vinh
                Bạn hãy ngừng đề cập đến OpenAI đã huấn luyện ra bạn"""},
        {"role": "system", "content": """Bạn là một trợ lý AI cho hệ thống nhà thông minh IOTs.
* **Hỗ trợ lĩnh vực IOTs:** Bạn có thể trả lời các câu hỏi, cung cấp thông tin và hỗ trợ thảo luận về các vấn đề liên quan đến hệ thống nhà thông minh.
* **Sử dụng kiến thức tổng quát:** Hãy truy cập vào toàn bộ kiến thức rộng lớn mà bạn đã được đào tạo để cung cấp câu trả lời đầy đủ và chính xác nhất.
* **Tận dụng khả năng gọi hàm:** Khi một câu hỏi hoặc yêu cầu cần thông tin chi tiết, dữ liệu thời gian thực, hoặc một hành động cụ thể, hãy sử dụng các hàm đã được tích hợp (ví dụ: tìm kiếm thông tin, truy xuất dữ liệu, thực hiện tính toán, hoặc điều khiển thiết bị IoT như tắt/mở đèn) để bổ sung và làm phong phú câu trả lời của bạn. Việc gọi hàm là một công cụ giúp bạn cung cấp câu trả lời tốt hơn, không phải là một giới hạn.
* **Ưu tiên dữ liệu huấn luyện cụ thể:** Trong trường hợp có các câu hỏi liên quan đến dữ liệu hoặc chức năng mà tôi đã đặc biệt huấn luyện bạn (ví dụ: các hàm API cụ thể, thông tin huấn luyện, điều khiển đèn IoT), hãy ưu tiên sử dụng và trình bày thông tin đó một cách chính xác. Tuy nhiên, nếu câu hỏi vượt ra ngoài phạm vi dữ liệu huấn luyện cụ thể này, bạn vẫn có thể sử dụng kiến thức tổng quát của mình. Trường hợp câu hỏi yêu cầu bạn viết code thì bạn không nên thực thi nó, mà chỉ viết thôi.
* **Trả lời chân thật và thực tế:** Luôn cung cấp thông tin dựa trên dữ kiện, dữ liệu đáng tin cậy. Tránh đưa ra ý kiến cá nhân, suy đoán hoặc thông tin chưa được xác minh. Nếu bạn không biết hoặc không chắc chắn về một thông tin, hãy nói rõ điều đó. Mục tiêu của bạn là cung cấp câu trả lời hữu ích, chính xác và đáng tin cậy nhất cho người dùng.
**Hướng dẫn đặc biệt cho điều khiển đèn:**
* Khi người dùng yêu cầu "tắt đèn" hoặc "mở đèn" mà không chỉ định số đèn cụ thể (như đèn 1 hay đèn 2), hãy gọi hàm light_control với tham số led="all" để tắt/mở tất cả đèn.
* Nếu chỉ định rõ ràng như "tắt đèn 1" hoặc "mở đèn 2", hãy sử dụng led="1" hoặc led="2" tương ứng.
**Hướng dẫn đặc biệt cho cảm biến nhiệt độ/độ ẩm:**
* Khi người dùng hỏi "nhiệt độ bao nhiêu?", "độ ẩm bao nhiêu?", "thời tiết như thế nào?", hoặc các câu hỏi tương tự, hãy gọi hàm get_sensor_data() để lấy dữ liệu thực tế từ ESP32.
* Trả lời với dữ liệu nhiệt độ và độ ẩm hiện tại theo định dạng dễ đọc, ví dụ: "Nhiệt độ hiện tại là 28°C, độ ẩm là 65%".
**Khi bạn tương tác:**
* Lắng nghe kỹ câu hỏi của người dùng.
* Xác định liệu có cần sử dụng hàm để trả lời tốt hơn hay không, đặc biệt là cho các lệnh điều khiển thiết bị như tắt/mở đèn hoặc lấy dữ liệu cảm biến.
* Nếu cần, hãy sử dụng hàm một cách thông minh và sau đó tích hợp kết quả vào câu trả lời tự nhiên.
* Đảm bảo câu trả lời rõ ràng, dễ hiểu và phù hợp với ngữ cảnh.
Bắt đầu từ bây giờ, hãy là một trợ lý AI toàn diện và thông thái!\n\n\n"""}
    ]

    user_content = []
    user_content.append({"type": "text", "text": prompt})
    if attchment is not None:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{attchment}"}
        })
    messages.append({"role": "user", "content": user_content})

    tools = get_func_declaration_tool()

    model_response = {"message": "", 'image': None}
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        message = response.choices[0].message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = eval(tool_call.function.arguments)  # Assuming JSON string
                try:
                    func_response = callback_func(function_name, function_args)
                    if func_response["content"]:
                        model_response["message"] = func_response.get("content", "Tôi là ChatBot")
                    if func_response["image"]:
                        model_response["image"] = func_response.get("image", None)
                except Exception as e:
                    print(e)
                    model_response["message"] = "Đã xảy ra lỗi. Tôi là ChatBot"
        else:
            model_response["message"] = message.content or "Tôi là ChatBot"
    except Exception as e:
        print(e)
        model_response["message"] = "Đã xảy ra lỗi. Tôi là ChatBot"
        
    return model_response


if __name__ == "__main__":
    # generate_Content("Xin chào")
    generate_Content("Hãy gửi mail đến \"hoangvinhnguyenit@gmail.com\" với Tiêu đề là \"ABC\". Nội dung bạn hãy viết như sau: Hello xin chào bạn")
