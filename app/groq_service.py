import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def generate_task_description(title: str):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": (
    "Write a short, clear, plain-text description for this task. "
    "Do not use Markdown, bold text, headings, bullet points, or special formatting. "
    f"Task: {title}"
)
                    }
                ],
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception:
            if attempt == max_retries - 1:
                raise
def generate_task_summary(description: str):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Summarize the following task description "
                            "in one short and clear sentence:\n\n"
                            f"{description}"
                        )
                    }
                ],
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception:
            if attempt == max_retries - 1:
                raise