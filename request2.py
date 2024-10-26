import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

history = []

def generate_adaptive_quiz(user_response, performance_feedback):
    # Create a prompt to generate questions based on performance feedback
    prompt = f"Generate a quiz question based on the student's performance:\n\nPerformance feedback: {performance_feedback}\nStudent response: {user_response}"
    history.append(prompt)

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
        print("Error:", response.text)
        return "An error occurred while generating the quiz question."

def generate_mini_tutorial(question):
    # Create a prompt to generate a mini-tutorial based on the user's question
    prompt = f"Provide a concise, topic-specific tutorial for the following question:\n\nQuestion: {question}"
    history.append(prompt)

    data = {
        "model": "Shiksha",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        mini_tutorial = data['response']
        return mini_tutorial
    else:
        print("Error:", response.text)
        return "An error occurred while generating the mini-tutorial."

# Gradio interface for Adaptive Quiz and Mini-Tutorial Generation
with gr.Blocks() as interface:
    gr.Markdown("## Personalized Learning Content Creation")
    
    with gr.Tab("Adaptive Quiz Generation"):
        user_response = gr.Textbox(lines=2, placeholder="Enter your response to the last question")
        performance_feedback = gr.Textbox(lines=2, placeholder="Enter feedback on student's performance")
        adaptive_quiz_output = gr.Textbox(lines=100, label="Generated Adaptive Quiz Question")
        
        quiz_button = gr.Button("Generate Quiz Question")
        quiz_button.click(generate_adaptive_quiz, inputs=[user_response, performance_feedback], outputs=adaptive_quiz_output)
    
    with gr.Tab("Mini-Tutorial Generation"):
        question = gr.Textbox(lines=2, placeholder="Enter the topic or question")
        tutorial_output = gr.Textbox(label="Generated Mini-Tutorial")
        
        tutorial_button = gr.Button("Generate Mini-Tutorial")
        tutorial_button.click(generate_mini_tutorial, inputs=question, outputs=tutorial_output)

interface.launch()
