from flask import Flask, request, render_template_string, jsonify, render_template, session
import os
from utils import save_file, read_file
from rag_engine import chunk_text, create_vector_store, process_and_answer
import glob
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

UPLOAD_FOLDER = os.path.join('data', 'uploaded_files')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    return render_template('landing.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('landing.html', 
                                  upload_message="No file uploaded", 
                                  upload_message_class="error")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('landing.html', 
                                  upload_message="No file selected", 
                                  upload_message_class="error")
    
    try:
        print(f"Debug: Original filename: {file.filename}")  # Debug line
        file_path = save_file(file)
        print(f"Debug: Saved to: {file_path}")  # Debug line
        
        # Print the extension of the saved file
        file_extension = os.path.splitext(file_path)[1].lower()
        print(f"Debug: Saved file extension: {file_extension}")
        
        text = read_file(file_path)
        if not text:
            return render_template('landing.html', 
                                      upload_message="File is empty", 
                                      upload_message_class="error")
        
        chunks = chunk_text(text)
        create_vector_store(chunks)
        
        return render_template('landing.html', 
                                   upload_message="File uploaded successfully!", 
                                   upload_message_class="success")
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug line
        return render_template('landing.html', 
                                  upload_message=f"Error: {str(e)}", 
                                  upload_message_class="error")
@app.route('/query', methods=['POST'])
def query():
    user_query = request.form.get('query', '').strip()
    if not user_query:
        return render_template('landing.html', 
                                   response="Please enter a question")
    
    try:
        response = process_and_answer(user_query)
        return render_template('landing.html', response=response)
    except Exception as e:
        return render_template('landing.html', 
                                   response=f"Error processing your query: {str(e)}")

@app.route('/chat', methods=['GET'])
def chat_page():
    return render_template('chat.html')

@app.route('/chat_api', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message', 'history': session.get('history', [])}), 400

    # Get or initialize chat history
    history = session.get('history', [])
    history.append({'role': 'user', 'content': user_message})

    try:
        assistant_response = process_and_answer(user_message)
    except Exception as e:
        assistant_response = f"Error: {str(e)}"

    history.append({'role': 'assistant', 'content': assistant_response})
    session['history'] = history

    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)