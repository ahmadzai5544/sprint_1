import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app UI
st.set_page_config(page_title="🎯 AI Interview Practice App", layout="centered")
st.title("🎯 AI Interview Practice App")
st.subheader("Prepare for your next job interview using AI!")

# Input fields
job_title = st.text_input("Enter job title:", placeholder="e.g. Data Analyst")
difficulty = st.selectbox("Select difficulty:", ["Easy", "Medium", "Hard"])
temperature = st.slider("Creativity level (temperature)", 0.0, 1.0, 0.5)

# Function to call OpenAI
def generate_questions(job_title, difficulty, temp):
    prompt = (
        f"Generate {difficulty.lower()} level job interview questions for the position of '{job_title}'. "
        f"Return the questions as a numbered list."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates interview questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=temp
    )

    return response['choices'][0]['message']['content']

# Button to generate output
if st.button("Generate Questions"):
    if not job_title.strip():
        st.warning("⚠️ Please enter a job title.")
    else:
        with st.spinner("Generating interview questions..."):
            try:
                output = generate_questions(job_title, difficulty, temperature)
                st.success("✅ Questions generated successfully!")
                st.markdown(output)
            except Exception as e:
                st.error(f"❌ Error: {e}")
