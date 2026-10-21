🌍 Bilingual Weekly Newsletter

An automated bilingual newsletter powered by Python, OpenAI, and GitHub Actions.

一个基于 Python、OpenAI 和 GitHub Actions 的自动化中英文双语周刊项目。

✨ Features

- 📰 Search for recent news and developments.
- 🇨🇳 Generate a Chinese weekly newsletter.
- 🇺🇸 Generate an English version covering the same stories.
- 🤖 Use AI to summarize news and explain why it matters.
- 📚 Learn five useful English expressions every week.
- 📧 Automatically deliver the newsletter by email.
- 🗂️ Archive each issue in the GitHub repository.
- ⏰ Run automatically every Saturday at 07:00 Beijing time.

🛠️ Tech Stack

- Python
- OpenAI Responses API
- OpenAI Web Search
- GitHub Actions
- SMTP email delivery

📂 Project Structure

.
├── .github/
│   └── workflows/
│       └── weekly.yml
├── newsletters/
├── newsletter.py
├── requirements.txt
└── README.md

⚙️ Configuration

Configure the following GitHub repository secrets:

- "OPENAI_API_KEY"
- "EMAIL_FROM"
- "EMAIL_TO"
- "EMAIL_PASSWORD"

Optional repository variables:

- "OPENAI_MODEL"
- "SMTP_HOST"
- "SMTP_PORT"

For Gmail, use "smtp.gmail.com" and port "465".

Use an appropriate Gmail app password if your account supports it.

Never commit API keys, email passwords, or other secrets to the repository.

⏰ Schedule

The workflow uses UTC scheduling:

- cron: "0 23 * * 5"

This corresponds to Saturday at 07:00 in Beijing time.

GitHub Actions scheduling may be delayed during periods of high load.

🚀 Manual Execution

1. Open the repository on GitHub.
2. Select the Actions tab.
3. Open Bilingual Weekly Newsletter.
4. Click Run workflow.

📚 Newsletter Archive

Generated issues are saved in the "newsletters/" directory.

Each issue is stored as a Markdown file named by date.

🔒 Security

Credentials are stored in GitHub Actions Secrets and are not hardcoded in the source code.

📄 License

MIT License
                             chy
                      2026 10 21         