import requests
import re
from datetime import datetime
from config import MAILGUN_API_KEY, MAILGUN_DOMAIN

def send_email(body, EMAIL_RECEIVER, EMAIL_TITLE):
    print("Sending email...")
    try:
        # 使用正则表达式清理 body 中的 Markdown 代码块标记
        cleaned_body = re.sub(r'```(?:html)?', '', body)  # 删除 ``` 和 ```html

        custom_date = datetime.now().strftime('%Y-%m-%d')

        # 配置邮件参数
        data = {
            "from": f"LifeSync-AI <noreply@{MAILGUN_DOMAIN}>",
            "to": [EMAIL_RECEIVER],
            "subject": f"{EMAIL_TITLE} {custom_date}",
            "html": cleaned_body
        }

        # 发送邮件请求到 Mailgun API
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=data
        )
        
        # 日志打印，用于调试
        print(f"Request URL: https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("Email sent successfully!")
        elif response.status_code == 401:
            print("Authentication failed. Please check your MAILGUN_API_KEY and MAILGUN_DOMAIN.")
        elif response.status_code == 403:
            print("Permission denied. Ensure the recipient is authorized (for free accounts).")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print("An error occurred while sending the email:")
        print(e)