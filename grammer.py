import requests
import json
import gradio as gr

# API endpoint for the Shiksha model
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

# Function to generate suggestions for grammar and style
def check_grammar_and_style(text):
    prompt = f"Please identify any grammatical errors and suggest stylistic improvements for the following text:\n\n{text}"
    
    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        suggestions = data['response']
        return suggestions
    else:
        return "Error: " + response.text

# Gradio interface for grammar and style checking
interface = gr.Interface(
    fn=check_grammar_and_style,
    inputs=gr.Textbox(lines=5, placeholder="Enter your text for grammar and style checking..."),
    outputs="text",
    title="Grammar and Style Checker",
    description="Enter your text and get suggestions for grammatical errors and stylistic improvements."
)

# Launch the Gradio interface
interface.launch()
