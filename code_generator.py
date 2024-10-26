import requests
import json
import gradio as gr

# API endpoint for the Shiksha model
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

# Function to generate code based on user input
def generate_code(prompt):
    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        generated_code = data['response']
        return generated_code
    else:
        return "Error: " + response.text

# Gradio interface for code generation
interface = gr.Interface(
    fn=generate_code,
    inputs=gr.Textbox(lines=5, placeholder="Describe your programming task or request code..."),
    outputs="code",
    title="Code Generation Assistant",
    description="Enter a programming task description, and the model will generate a code snippet for you."
)

# Launch the Gradio interface
interface.launch()
