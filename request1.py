import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

history = []

def summarize_text(text):
    # Prepare the prompt for summarization
    prompt = f"Summarize the following text:\n\n{text}"
    history.append(prompt)  # Keeping track of prompts if needed

    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_summary = data['response']
        return actual_summary
    else:
        print("Error:", response.text)
        return "An error occurred while generating the summary."

interface = gr.Interface(
    fn=summarize_text,
    inputs=gr.Textbox(lines=10, placeholder="Enter text to summarize"),
    outputs="text",
    title="Text Summarization",
    description="Enter a piece of text and get a concise summary."
)

interface.launch()
