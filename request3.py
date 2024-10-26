import streamlit as st
import fitz  # PyMuPDF
import random
import re

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text += page.get_text("text")
            return text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

# Function to generate meaningful MCQ questions from extracted text
def generate_mcq_questions(extracted_text, difficulty="medium", num_questions=5):
    questions = []
    sentences = re.split(r'(?<=[.!?]) +', extracted_text)  # Split text into sentences
    important_sentences = [s for s in sentences if len(s.split()) > 5]  # Filter out short sentences

    for i in range(min(num_questions, len(important_sentences))):
        sentence = important_sentences[i]
        question_text = f"What is the main idea of the following statement: '{sentence.strip()}'?"

        # Generate answer choices
        choices = []
        for _ in range(3):  # Add 3 random choices based on sentence
            choices.append(generate_similar_statement(sentence))
        correct_answer = generate_similar_statement(sentence)  # Assume this is the correct answer
        choices.append(correct_answer)
        random.shuffle(choices)  # Shuffle choices

        question = {
            "question_text": question_text,
            "choices": choices,
            "correct_answer": correct_answer
        }
        questions.append(question)
    
    return questions

# Function to create a similar statement (dummy implementation)
def generate_similar_statement(original):
    words = original.split()
    random.shuffle(words)
    return ' '.join(words[:min(5, len(words))])  # Create a similar sentence

# Adaptive function to evaluate answers and determine next question difficulty
def evaluate_answers(questions, user_answers):
    correct_count = 0
    for i, question in enumerate(questions):
        if question["correct_answer"] == user_answers[i]:
            correct_count += 1
    # Determine difficulty for next set based on performance
    if correct_count >= len(questions) * 0.8:
        next_difficulty = "hard"
    elif correct_count >= len(questions) * 0.5:
        next_difficulty = "medium"
    else:
        next_difficulty = "easy"
    return correct_count, next_difficulty

# Streamlit UI
st.title("Adaptive PDF Quiz Generator")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf("uploaded.pdf")
    
    if pdf_text:
        st.write("Extracted Text:")
        st.text_area("Extracted Text", pdf_text[:1000], height=200)  # Display first 1000 chars

        # Start Quiz
        if st.button("Start Quiz"):
            # Initialize session state for questions and answers
            if 'questions' not in st.session_state:
                st.session_state.questions = generate_mcq_questions(pdf_text, difficulty="medium", num_questions=5)
                st.session_state.user_answers = [None] * len(st.session_state.questions)
                st.session_state.current_question_set = 1
            
            # Display generated questions as MCQs
            questions = st.session_state.questions
            user_answers = st.session_state.user_answers

            for i, question in enumerate(questions):
                if user_answers[i] is None:  # Only display unanswered questions
                    st.write(question["question_text"])
                    answer = st.radio(
                        f"Choose your answer for Question {i + 1}",
                        question["choices"],
                        key=f"question_{i}"
                    )
                    user_answers[i] = answer  # Save user's answer to session state

            # Submit answers and evaluate
            if st.button("Submit Answers"):
                score, next_difficulty = evaluate_answers(questions, user_answers)
                st.write(f"Your Score: {score}/{len(questions)}")
                st.write(f"Based on your performance, the next set of questions will be: {next_difficulty.capitalize()}")

                # Generate second set of questions based on performance
                st.session_state.questions = generate_mcq_questions(pdf_text, difficulty=next_difficulty, num_questions=5)
                st.session_state.user_answers = [None] * len(st.session_state.questions)
                st.session_state.current_question_set += 1

                st.experimental_rerun()  # Rerun the app to refresh with new questions

            # If it's the second set of questions
            if st.session_state.current_question_set == 2:
                questions = st.session_state.questions
                user_answers = st.session_state.user_answers

                for i, question in enumerate(questions):
                    if user_answers[i] is None:  # Only display unanswered questions
                        st.write(question["question_text"])
                        answer = st.radio(
                            f"Choose your answer for Question {i + 6}",
                            question["choices"],
                            key=f"question2_{i}"
                        )
                        user_answers[i] = answer  # Save user's answer to session state

                # Submit second set of answers and evaluate
                if st.button("Submit Second Set of Answers"):
                    score2, _ = evaluate_answers(questions, user_answers)
                    st.write(f"Your Score for Second Set: {score2}/{len(questions)}")
                    total_score = score + score2
                    st.write(f"Total Score: {total_score}/{len(questions) + 5}")

    else:
        st.write("Could not extract text from the PDF. Please upload a different file.")
else:
    st.write("Please upload a PDF file to start.")
