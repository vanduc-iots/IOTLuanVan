import smtplib, markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setup import EMAIL_ACCOUNT, EMAIL_PASSWORD
from logging.handlers import SMTPHandler 

def send_mail(to: list, subject, content, senderName = "Dịch Vụ Gửi Mail"):
    try:
        html_str = markdown.markdown(content)

        msg = MIMEMultipart()
        msg['From'] = senderName #EMAIL_ACCOUNT + f" <{senderName}>"
        msg['Subject'] = subject
        msg.attach(MIMEText(html_str, 'html'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        for mail in to:
            if isinstance(mail, dict):
                mail = mail.get("email")
            server.sendmail(EMAIL_ACCOUNT, mail, msg.as_string())
        print("Gửi Mail thành công")

    except Exception as e:
        print("Send Mail failed")
        print("Erorr content: ", e)
        raise e
    
    finally:
        server.quit()


# 1. Nội dung Markdown
markdown_content = """
# Chào mừng đến với email Markdown!

Đây là một ví dụ về cách gửi email với **nội dung Markdown** được chuyển đổi sang HTML.

* Mục 1
* Mục 2

Bạn có thể sử dụng các thẻ như **in đậm**, *in nghiêng*, và [liên kết](https://www.google.com).

Trân trọng,
Người gửi
"""

if __name__ == "__main__":
    html_str = markdown.markdown(markdown_content)
    msg = MIMEMultipart()
    msg['To'] = 'nguyennthts01667@gmail.com'
    msg['Subject'] = "Xin chào"
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
