import openai
import streamlit as st
import threading
import queue


openai.api_key = "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"


model_engine = "text-davinci-002"
prompt = "The Meditations of Marcus Aurelius"


def generate_response(prompt, model_engine, message):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt + f"\n\nUser: {message}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


def chat_thread(input_queue, output_queue):
    while True:
        message = input_queue.get()
        response = generate_response(prompt, model_engine, message)
        output_queue.put(response)


def app():
    st.title("STOIC CHAT BOT")
    st.write("Heyy I am chatbot trained on Meditaion written by Marcus Auriuells")
    
    input_queue = queue.Queue()
    output_queue = queue.Queue()
    
  
    thread = threading.Thread(target=chat_thread, args=(input_queue, output_queue))
    thread.start()

    messages = []

    while True:
        message = st.text_input("You:", key=f'input_{len(messages)}')
        if message:
            messages.append(message)
            input_queue.put(message)
            response = output_queue.get()
            st.write("Bot:", response)
        messages.clear() 

if __name__ == "__main__":
    app()

