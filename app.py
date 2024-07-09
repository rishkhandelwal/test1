# Updates to keyboard shortcuts … On Thursday 1 August 2024, Drive keyboard shortcuts will be updated to give you first-letter navigation.Learn more
from flask import Flask, request, jsonify
import docx
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

app = Flask(__name__)

def chat_with_openai(chat_history, docx_file):
    # Extract the text from the docx file
    doc = docx.Document(docx_file)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    user_input = request.json['user_input']
    # Create a prompt from the text
    prompt = [{"role": "system","content": """ Keep your answers very short, compact and concise. 
    Your answers should be deep into the context of Business. 
    If the user asked for any content which belongs to a different Coach, you should guide them to check out the Coach related to the input. 
    Dont comment on prompt(input). Provide response as a human would.
    Dont reply to negative questions regarding any religion."""}, {"role": "user", "content": text + user_input}]
    # Call the Groq API
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=prompt
    )
    # Return the response
    response = chat_completion.choices[0].message.content
    sentences = response.split('. ')

    # Return the sentences as a list
    return jsonify({'response': sentences})

@app.route('/api/manager-chat=4', methods=['POST'])
def chat():
    docx_file = request.json['docx_file']
    return chat_with_openai(None, docx_file)
