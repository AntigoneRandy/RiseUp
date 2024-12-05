from notion_client import Client
from datetime import datetime, timedelta

def fetch_tasks_from_notion(custom_date, USER_NOTION_TOKEN, USER_DATABASE_ID):
    notion = Client(auth=USER_NOTION_TOKEN)
    print("\nFetching tasks from Notion...\n")
    try:
        results = notion.databases.query(
            database_id=USER_DATABASE_ID
        )
        
        tasks_to_do = []
        tasks_to_record = []

        # 定义日期范围
        today = custom_date

        for row in results["results"]:
            if 'date' in row['properties']['Date'] and row['properties']['Date']['date']:
                task_date = datetime.strptime(row['properties']['Date']['date']['start'], '%Y-%m-%d').date()
                
                # 检查任务日期
                if task_date == today:
                    task = {
                        'To Do': row['properties']['To Do']['rich_text'][0]['text']['content'] if 'rich_text' in row['properties']['To Do'] and row['properties']['To Do']['rich_text'] else 'No To Do',
                        'Date': task_date.strftime('%Y-%m-%d')
                    }
                    tasks_to_do.append(task)
                elif task_date == today - timedelta(days=1):
                    task = {
                        'To Record': row['properties']['To Record']['rich_text'][0]['text']['content'] if 'rich_text' in row['properties']['To Record'] and row['properties']['To Record']['rich_text'] else 'No Record',
                        'Date': task_date.strftime('%Y-%m-%d')
                    }
                    tasks_to_record.append(task)

        print("Fetching success.")
        # print(tasks_to_do)
        # print(tasks_to_record)
        return {
            "tasks_to_do": tasks_to_do,
            "tasks_to_record": tasks_to_record
        }
    except Exception as e:
        print(f"Error fetching data from Notion: {e}")
        return {"tasks_to_do": [], "tasks_to_record": []}
