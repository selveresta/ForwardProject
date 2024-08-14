from openai import OpenAI
from config.config import OPENAI_API_KEY


class GPTClient:
    client = OpenAI(api_key=OPENAI_API_KEY)

    def __init__(self):
        pass

    def generate_comments_by_post(self, post_text):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a content maker"},
                {
                    "role": "user",
                    "content": f"Write a comments to post under and separate it by ','\n\n {post_text}",
                },
            ],
        )
        print(completion.choices[0].message)


# gpt = GPTClient()
