import re

def markdown_to_plain_text(markdown_text):
    # 移除 Markdown 特定标记（如 ##、*、- 等）
    plain_text = re.sub(r'#+\s', '', markdown_text)  # 去除标题符号 (如 ## )
    plain_text = re.sub(r'\*\s*', '', plain_text)    # 去除无序列表符号 (如 * )
    plain_text = re.sub(r'\\\d+\.', '', plain_text)  # 去除转义的数字列表符号 (如 1\.)
    plain_text = re.sub(r'\s*\n\s*', '\n', plain_text)  # 去除多余空白
    return plain_text.strip()

def markdown_to_notion_blocks(markdown_text):
    blocks = []
    for line in markdown_text.splitlines():
        line = clean_markdown_line(line)  # 清理每一行的 Markdown 转义符号

        if line.startswith("## "):  # 二级标题
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": line[3:]}  # 去掉 "## " 前缀
                        }
                    ]
                }
            })
        elif line.startswith("### "):  # 三级标题
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": line[4:]}  # 去掉 "### " 前缀
                        }
                    ]
                }
            })
        elif line:  # 普通段落
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": line}
                        }
                    ]
                }
            })
    return blocks


def clean_markdown_line(line):
    # 移除转义符号
    line = re.sub(r'\\\.', '.', line)  # 移除数字列表的转义符
    line = re.sub(r'\\-', '-', line)  # 移除无序列表的转义符
    return line.strip()