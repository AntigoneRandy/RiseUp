# RiseUp

## English README
## 中文 README

### 概览

你想在每天早上醒来后的第一件事，不是漫无目的的刷小红书或者朋友圈吗？

你希望早上一起床看到的是一段对昨日事件和你所有的东西的感恩以及长期目标的提醒吗？

你希望早上能看到天气以及穿搭建议，以及对今日任务的总结和完成建议吗？

**试试 RiseUp 吧！** 如果你本身就是 Notion 用户，那么它的部署会非常容易！

RiseUp 是一款集成 AI 技术的个人生产力和幸福感提升工具。用户在配置基础信息之后，例如：

- 个人作息
- 长期目标
- 基础信息

每天晚上记录当天觉得值得记录的事件，并且安排好第二天的 To-do List。第二天早上，用户会收到一封包含以下内容的邮件：

- 感恩提醒
- 长期目标提醒
- 天气信息
- 时间管理建议
- 今日任务列表

此外，用户还可以选择将这些信息更新到 Notion 中。

### 主要功能
- **AI助手**：集成智能AI助手，提供个性化的任务建议、日程优化及激励。
- **每日邮件通知**：每天早晨自动发送任务和建议邮件，确保你开始每一天时都清晰明了。
- **Notion更新**：也可以选择不发邮件，每天更新在notion的固定Page中，该参数在用户信息配置界面中设置。
- **感恩提醒**：会根据用户的基本信息和昨日完成的事件，生成一段感恩提醒，顺便根据昨日完成的记录事件对我进行鼓励
- **长期目标提醒**：会根据用户的基本信息和长期目标，生成一段关于长期目标的提醒和激励内容。
- **天气信息**：根据实时天气更新提供定制化建议，帮助你安排合适的户外活动或出行计划。
- **定制化环境变量**：自动获取并管理用户环境变量，支持多用户个性化配置。
- **时间管理建议**：根据用户的 今日任务列表和日常作息安排，提供详细的时间分配和建议。

### 入门指南

#### 先决条件
- Python 3.8+ （云端部署不需要）
- Notion API密钥（申请方式可见下方用户信息配置界面中所述）
- Mailgun API密钥（在 Mailgun 官网申请）
- 智谱 AI API密钥（只要在配置信息时api选GLM-4-Flash就是Free的！）
- OpenWeather API密钥（在 OpenWeather 官网申请）

#### 配置
首��，打开下列页面并复制到Notion后修改为自己的信息


-[用户信息配置界面（必须）](https://ink-specialist-007.notion.site/153066b3cc81800fb066fd6686711042?v=153066b3cc818172a648000c0a67f832&pvs=4)
-[任务数据库模板（必选）](https://ink-specialist-007.notion.site/Daily-Dashboard-1-153066b3cc818035a167c888fd161db3?pvs=4)
### 安装及运行
1. **本地运行（不推荐）**
   首先，Fork此仓库并安装所需依赖：
   ```bash
   git clone https://github.com/YourUsername/RiseUp.git
   cd RiseUp
   conda create -n riseup python=3.10
   conda activate riseup
   pip install -r requirements.txt
   ```
   然后配置 .env 文件以设置您的Notion Token、ZhipuAI密钥和OpenWeather API密钥。

   运行以下命令以启动程序：
   ```bash
   python main.py
   ```
   确保 .env 中的所有配置正确无误。

2. **云端运行（推荐）**
   在GitHub右上角Fork此仓库。

   修改 .github/workflows/deploy.yml 文件中的定时启动时间：
   ```yaml
   on:
     schedule:
       - cron: '0 22 * * *'
     workflow_dispatch:
   ```
   这里的 cron 表示每日的启动时间（以UTC时间为准，例如 cron: '0 22 * * *' 代表北京时间早上6点）。

   进入 Settings -> Secrets and Variables -> Repository secrets 配置以下变量：
   - NOTION_DATABASE_ID
   - NOTION_TOKEN
   - MAILGUN_API_KEY
   - MAILGUN_DOMAIN
   - OPENAI_API_KEY
   - OPENWEATHER_API_KEY

   程序将按照设定的时间自动运行，您也可以手动触发运行。在 Actions -> Daily Report -> Run Workflow 页面中点击运行。

### 贡献
该项目部分重构了[这个项目](https://github.com/Zippland/LifeSync-AI),非常感谢这个作者！并且我欢迎各种形式的贡献。要贡献，请：
- Fork仓库。
- 创建功能分支。
- 如果您添加了新功能，请确保添加相关测试。
- 遵循项目的编码规范。
- 提交Pull Request。

### 许可证
根据 Apache 许可证 许可。

### 联系方式
如需支持或查询，请通过 jackyofgrj@gmail.com 与我联系。