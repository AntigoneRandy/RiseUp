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
                "请生成一个以<h2>开头的段落，内容应包含感恩提醒并根据昨日完成的记录事件对我进行鼓励。"
                "提醒我对生活中值得感激的事物心怀感恩，重点突出感恩，并以积极和温暖的语气进行表达：\n"
                "1. 根据我的基本信息，提到生活中的具体美好事物。\n"
                "2. 从昨日的记录中提取完成的事情，并鼓励我继续保持。\n\n"
                f"输入数据(关于我的简介和昨日完成事情的记录)：{data}\n"
            ),
            "goals": (
                "请生成一个以<h2>开头的段落，描述我的长期目标的提醒和激励内容。请对每一个目标分别用<h3>段落单独描述，确保结构清晰，并突出每个目标的意义和达成后的积极影响：\n"
                "根据我的基本信息，为目标的意义提供情感化连接（如我的背景和动机）。\n"
                "对每一个长期目标，描述其重要性，并给予鼓励或激励语言。\n"
                "每个目标的描述应具体、积极，同时让人感到希望和动力。\n\n"
                f"输入数据：{data}\n"
            ),
            "weather": (
                "请在一个h2段落内总结今天的天气情况，然后给我当天的穿搭建议、出行建议及注意事项（可能包括穿搭、防晒、雨具、防风等等）"
                f"天气数据：{data}\n"
            ),
            # "tasks": (
            #     "请生成一段以<h2>开头的HTML格式内容，总结我的今日待办事项并提供详细的时间安排建议。"
            #     "请根据以下要求生成内容：\n"
            #     "1. 对今日任务列表进行分类或排序（如优先级、紧急程度等）。\n"
            #     "2. 结合我的日常作息，合理安排任务的时间，并生成清晰的时间轴或日程表。\n"
            #     "3. 提供简短的任务描述，以及完成任务时的注意事项或小贴士。\n"
            #     "4. 用积极和鼓励的语气，激励我高效完成任务。\n"
            #     "5. 必须使用<h3>标注关键任务类别，时间轴用<ul>结构呈现。\n\n"
            #     f"输入数据：{data}\n"
            # )
            "tasks": (
                "请根据以下信息生成一段关于今日待办事项的总结和时间安排建议，用积极和鼓励的语气，激励我高效完成任务，待办事项总结可以附上注意事项或小贴士：\n"
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