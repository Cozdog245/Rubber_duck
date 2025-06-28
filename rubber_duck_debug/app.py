import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Gets api key from env file

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html') #returns HTML content from index.html

@app.route('/test')
def test_openai(): # to pull information from openai
    try:
        response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = [{"role": "user", "content": "I'm a programmer with a bug. Introduce yourself as my rubber duck helper."}],
            max_tokens = 10
        )
        return f"OpenAI says: {response.choices[0].message.content}"
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    return f'You said:{user_message}'

if __name__ == '__main__':
    app.run()