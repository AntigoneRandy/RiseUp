import re

def markdown_to_notion_blocks(markdown_text):
    blocks = []
    lines = markdown_text.splitlines()
    
    # 打印拆分后的每一行
    print("\n[DEBUG] Splitting markdown into lines:")
    for i, line in enumerate(lines):
        print(f"  Line {i+1}: {line}")
    
    for line in lines:
        if line.startswith("## "):  # 处理二级标题
            print(f"\n[DEBUG] Detected heading_2: {line}")
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": line[3:]}  # 去掉 ## 后的标题内容
                    }]
                }
            })
        elif line.startswith("### "):  # 处理三级标题
            print(f"\n[DEBUG] Detected heading_3: {line}")
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": line[4:]}  # 去掉 ### 后的标题内容
                    }]
                }
            })
        elif line.strip():  # 处理普通段落
            print(f"\n[DEBUG] Detected paragraph: {line}")
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": line.strip()}
                    }]
                }
            })
    
    # 打印生成的 Notion 块结构
    print("\n[DEBUG] Generated Notion blocks:")
    for block in blocks:
        print(block)
    
    return blocks