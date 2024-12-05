import re
from zhipuai import ZhipuAI
from config import OPENAI_API_KEY

def generate_advice_with_gpt(advice_part, data, gpt_version,user_name):
    print("\nGenerating advice with GPT...")
    try:
        client = ZhipuAI(api_key=OPENAI_API_KEY)  # 使用智谱AI客户端
        
        # Define prompts based on advice_part
        prompts = {
            "gratitude": (
                "请在一个h2段落内根据以下信息生成一段感恩提醒，顺便根据昨日完成的记录事件对我进行鼓励，主要是感恩提醒：\n"
                "1. 关于我的基本信息。\n"
                "2. 昨日完成的记录。\n\n"
                f"输入数据：{data}\n"
            ),
            "goals": (
                "请在一个h2段落内根据以下信息生成一段关于长期目标的提醒和激励内容，请注意每一个长期目标都用一个h3段落来描述：\n"
                "1. 我的基本信息。\n"
                "2. 我的长期目标。\n\n"
                f"输入数据：{data}\n"
            ),
            "weather": (
                "请在一个h2段落内总结今天的天气情况，然后给我当天的穿搭建议、出行建议及注意事项（可能包括穿搭、防晒、雨具、防风等等）"
                f"天气数据：{data}\n"
            ),
            "tasks": (
                "请根据以下信息生成一段关于今日待办事项的总结和时间安排建议：\n"
                "1. 今日任务列表。\n"
                "2. 我的日常作息。\n\n"
                f"输入数据：{data}\n"
            )
        }

        prompt = prompts.get(advice_part, "")
        
        response = client.chat.completions.create(
            model=gpt_version,
            messages=[
                # {"role": "system", "content": "你是我的日程秘书，请根据以下指令生成内容。请使用HTML格式，结构清晰，不要问候语或多余信息,注意！使用中文返回。"},
                {"role": "system", "content": f"你是一个富有同理心和情感智慧的日程助手，致力于帮助用户以最愉悦和充实的方式开始新的一天，用户的名字是{user_name}。你的目标是通过温暖、积极且条理清晰的建议，为用户提供有用的信息，同时激发对未来的期待。请在生成内容时适度使用表情符号（如🌞、📚、💪等），以增强内容的情感表达和趣味性。注意保持语气真诚而贴心，避免过度使用表情符号或显得过于随意。输出格式为HTML，仅包含内容的<body>部分，无需任何开场白、称呼或问候语，注意用中文返回！"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.3
        )
        
        print("Generated response.")
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            cleaned_message = re.sub(r'<body>|</body>|```html?|```', '', message_content)
            print(cleaned_message)
            return cleaned_message
        else:
            return "No advice generated."
    
    except Exception as e:
        print(f"Error generating advice: {e}")
        return "Error occurred during generation."