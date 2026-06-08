# Hướng Dẫn Tích Hợp Lệnh Bằng Giọng Nói

## 📝 Giới Thiệu

Chatbot của bạn đã được tích hợp tính năng **nhận lệnh bằng giọng nói** sử dụng **Web Speech API**. Người dùng có thể:
- Nhấp nút "Ghi âm" để bắt đầu ghi âm giọng nói
- Hệ thống sẽ tự động chuyển đổi giọng nói thành văn bản
- Tin nhắn sẽ tự động được gửi tới chatbot

## 🎯 Các Tính Năng

### 1. **Ghi Âm Giọng Nói**
   - Nhấp nút "Ghi âm" trong menu (dấu +) ở góc dưới bên phải
   - Nút sẽ chuyển thành màu đỏ và hiển thị "Đang lắng nghe..."
   - Nói rõ ràng lệnh hoặc câu hỏi của bạn

### 2. **Chuyển Đổi Tự Động**
   - Giọng nói được chuyển thành văn bản trong thời gian thực
   - Hỗ trợ tiếng Việt mặc định

### 3. **Gửi Tự Động**
   - Sau khi dừng ghi âm, tin nhắn sẽ tự động được gửi
   - Chatbot sẽ phản hồi ngay lập tức

## 🛠️ Cấu Trúc Kỹ Thuật

### Các File Được Thêm/Sửa Đổi:

1. **`static/voice-recognition.js`** - Module nhận dạng giọng nói
   - Sử dụng Web Speech API
   - Hỗ trợ các ngôn ngữ khác nhau
   - Xử lý các sự kiện giọng nói

2. **`templates/home.html`** - Cập nhật nút ghi âm
   - Thêm ID và icon cho nút voice
   - Thêm hiển thị trạng thái

3. **`static/scripts.js`** - Thêm xử lý sự kiện giọng nói
   - Lắng nghe sự kiện nút ghi âm
   - Cập nhật UI trong quá trình ghi âm
   - Gửi tin nhắn tự động

4. **`templates/layout.html`** - Thêm script reference
   - Tải voice-recognition.js trước scripts.js

5. **`static/style.css`** - Thêm styling cho voice button
   - Animation giờ vàng khi đang lắng nghe
   - Hiệu ứng xung động lên/xuống

## 📋 Yêu Cầu Trình Duyệt

Web Speech API được hỗ trợ trên:
- ✅ Chrome/Chromium (v25+)
- ✅ Edge (v79+)
- ✅ Opera (v27+)
- ✅ Safari (v14.1+)
- ❌ Firefox (không hỗ trợ)

## ⚙️ Cấu Hình

### Thay Đổi Ngôn Ngữ

Để thay đổi ngôn ngữ, mở `static/voice-recognition.js` và chỉnh sửa:

```javascript
this.recognition.language = 'vi-VN'; // Thay vi-VN bằng mã ngôn ngữ khác
```

**Mã ngôn ngữ phổ biến:**
- `vi-VN` - Tiếng Việt
- `en-US` - Tiếng Anh (Mỹ)
- `fr-FR` - Tiếng Pháp
- `de-DE` - Tiếng Đức
- `es-ES` - Tiếng Tây Ban Nha
- `ja-JP` - Tiếng Nhật
- `zh-CN` - Tiếng Trung Quốc (Simplify)

### Tắt Gửi Tự Động

Nếu muốn người dùng tự ấn nút gửi, sửa trong `static/scripts.js`:

```javascript
// Comment out hoặc xóa dòng này:
// setTimeout(() => {
//     document.getElementById("send-message").click();
// }, 500);
```

## 🔊 Xử Lý Lỗi

Hệ thống sẽ hiển thị thông báo lỗi nếu:
- ❌ Không phát hiện âm thanh: "Không phát hiện âm thanh. Vui lòng thử lại."
- ❌ Không có microphone: "Không tìm thấy microphone."
- ❌ Lỗi kết nối: "Lỗi kết nối mạng."

## 🚀 Sử Dụng

1. Mở ứng dụng chatbot trong trình duyệt
2. Nhấp vào dấu `+` ở góc dưới bên phải input
3. Chọn "Ghi âm"
4. Nói rõ ràng lệnh/câu hỏi
5. Nó sẽ tự động gửi khi bạn dừng nói

## 🔐 Quyền Truy Cập

Lần đầu sử dụng, trình duyệt sẽ yêu cầu cấp quyền truy cập microphone. Hãy chọn "Cho phép" để tiếp tục.

## ⚡ Tối Ưu Hóa

Nếu muốn tích hợp thêm:

- **Text-to-Speech (Chuyển văn bản thành giọng nói)**: Thêm Web Speech Synthesis API
- **Nhận dạng lệnh cụ thể**: Thêm xử lý regex sau khi nhận được transcript
- **Lưu lịch sử giọng nói**: Thêm logging/database

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra ngoài không gây nhiễu
2. Kiểm tra microphone hoạt động bằng test âm thanh khác
3. Thử trình duyệt khác (Chrome được khuyên dùng)
4. Xem browser console (F12) để debug
