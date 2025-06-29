import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #Gets api key from env file

from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

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

    if 'chat_history' not in session:
        session['chat_history'] = []

    session['chat_history'].append({'role': 'user', 'content': user_message})

    messages= [
            {'role': 'system', 'content': 'You are a helpful rubber duck for debugging. Ask one clarifying question to help them think through their problem. Be encouraging and friendly.'},
    ] + session['chat_history'][-10:]

    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = messages,
        max_tokens=200
    )

    duck_response = response.choices[0].message.content

    session['chat_history'].append({'role': 'assistant', 'content': duck_response})

    return jsonify({'response': duck_response})

if __name__ == '__main__':
    app.run()
