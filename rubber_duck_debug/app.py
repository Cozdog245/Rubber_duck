import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return'<p>Hello, World!</p>'

@app.route('/test')
def test_openai():
    try:
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [{"role": "user", "content": "Say hello in one word"}],
            max_tokens = 10
        )
        return f"OpenAI says: {response.choices[0].message.content}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()