import requests
import json
import gradio as gr
from PyPDF2 import PdfReader

# API endpoint for the Shiksha model
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

# Function to read and extract text from a PDF file
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# Function to generate an adaptive quiz question
def generate_adaptive_quiz(user_response, performance_feedback):
    prompt = f"Generate a quiz question based on the student's performance:\n\nPerformance feedback: {performance_feedback}\nStudent response: {user_response}"
    
    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        generated_question = data['response']
        return generated_question
    else:
        return "Error: " + response.text

# Gradio interface for the Adaptive PDF Quiz Generator
def create_quiz(file, user_response, performance_feedback):
    extracted_text = extract_text_from_pdf(file)
    
    # Use the extracted text as context for quiz generation
    prompt = f"Based on the following content:\n{extracted_text}\n\nGenerate a quiz question based on the student's performance:\n\nPerformance feedback: {performance_feedback}\nStudent response: {user_response}"
    
    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        generated_question = data['response']
        return generated_question
    else:
        return "Error: " + response.text

# Gradio interface
with gr.Blocks() as interface:
    gr.Markdown("## Adaptive PDF Quiz Generator")
    
    with gr.Row():
        pdf_input = gr.File(label="Upload PDF File")
        user_response = gr.Textbox(lines=2, placeholder="Enter your response to the last question")
        performance_feedback = gr.Textbox(lines=2, placeholder="Enter feedback on student's performance")
        
    quiz_output = gr.Textbox(lines=5, label="Generated Adaptive Quiz Question")
    
    generate_button = gr.Button("Generate Quiz Question")
    generate_button.click(create_quiz, inputs=[pdf_input, user_response, performance_feedback], outputs=quiz_output)

# Launch the Gradio interface
interface.launch()
