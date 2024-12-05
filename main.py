import pytz
from src.send_information.format_email import format_email
from src.get_information.task_from_notion import fetch_tasks_from_notion
from src.send_information.email_notifier import send_email
from src.send_information.m2n import markdown_to_notion_blocks
from src.send_information.m2n import markdown_to_plain_text
from src.ai_generating.zhipuai_advice_generator import generate_advice_with_gpt
from src.get_information.get_wheather import get_weather
from datetime import datetime
from src.get_information.env_from_notion import get_user_env_vars

from notion_client import Client
import html2text


# Get the current time in UTC, and then convert to the specified UTC offset
utc_now = datetime.now(pytz.utc)
user_data = get_user_env_vars()


# 将 Markdown 转换为 Notion 块

for user_id in user_data:
    user_notion_token = user_data[user_id]["USER_NOTION_TOKEN"]
    user_database_id = user_data[user_id]["USER_DATABASE_ID"]
    gpt_version = user_data[user_id]["GPT_VERSION"]
    present_location = user_data[user_id]["PRESENT_LOCATION"]
    user_name = user_data[user_id]["USER_NAME"]
    custom_date = utc_now.astimezone(pytz.timezone('Etc/GMT-' + user_data[user_id]["TIME_ZONE"])).date()
    display_page_id = user_data[user_id]["DISPLAY_PAGE_ID"]
    display_way = user_data[user_id]["DISPLAY_WAY"]

    # Fetch tasks and environment data
    tasks = fetch_tasks_from_notion(custom_date, user_notion_token, user_database_id)
    today_tasks = tasks["tasks_to_do"]
    yesterday_records = tasks["tasks_to_record"]
    weather = get_weather(present_location)

    # Additional personal details
    about_me = user_data[user_id]["ABOUT_ME"]
    daily_routine = user_data[user_id]["DAILY_ROUTINE"]
    long_term_goal = user_data[user_id]["LONG_TERM_GOAL"]

    # Generate email parts using ChatGLM
    email_body = ""

    # Part 1: 感谢和鼓励
    gratitude_content = generate_advice_with_gpt(
        "gratitude", {"about_me": about_me, "yesterday_records": yesterday_records},
        gpt_version, user_name
    )
    email_body += format_email(gratitude_content) + "\n\n"

    # Part 2: 长期目标提醒
    goals_content = generate_advice_with_gpt(
        "goals", {"about_me": about_me, "long_term_goal": long_term_goal},
        gpt_version, user_name
    )
    email_body += format_email(goals_content) + "\n\n"

    # Part 3: 天气更新
    weather_content = generate_advice_with_gpt("weather", weather, gpt_version, user_name)
    email_body += format_email(weather_content) + "\n\n"

    # Part 4: 今天的待办事项
    tasks_content = generate_advice_with_gpt(
        "tasks", {"today_tasks": today_tasks, "daily_routine": daily_routine},
        gpt_version, user_name
    )
    email_body += format_email(tasks_content) + "\n\n"

    # 根据 DISPLAY_WAY 发送邮件或更新 Notion 页面
    if display_way == "email":
        send_email(email_body, user_data[user_id]["EMAIL_RECEIVER"], user_data[user_id]["EMAIL_TITLE"])
    elif display_way == "NOTION":
        # notion_client = Client(auth=user_notion_token)
        # # 转换 Markdown 为 Notion 块格式
        # email_body = html2text.html2text(email_body)
        # notion_blocks = markdown_to_notion_blocks(email_body)
        # # 插入到 Notion 页面
        # response = notion_client.blocks.children.append(
        #     block_id=display_page_id,
        #     children=notion_blocks
        # )
        # print("Inserted structured content into Notion page.")
        notion_client = Client(auth=user_notion_token)
        email_body = html2text.html2text(email_body)
        notion_blocks = markdown_to_plain_text(email_body)
        try:
            # 使用 append blocks 向页面添加内容
            response = notion_client.blocks.children.append(
                block_id=display_page_id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [  # 修复：显式定义 rich_text
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notion_blocks  # 插入的文字内容
                                    }
                                }
                            ]
                        }
                    }
                ]
            )
            print("Content added successfully to Notion page:", response)
        except Exception as e:
            print("Failed to add content to Notion page:", e)