# main.py
import os
from flask import Flask, request, jsonify, render_template, Response
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from gemini_llm import GeminiLLM
import google.generativeai as genai
import time
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage


app = Flask(__name__)

# Configure Gemini API for streaming
API_KEY = "AIzaSyC__4SYJyttUSRsszBXAscUULwfDbiv84M"
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
def stream_gemini_response(prompt):
    """
    Stream response from Gemini API - yields words as they arrive
    """
    try:
        response = gemini_model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                words = chunk.text.split()
                for word in words:
                    yield word + ' '
                    time.sleep(0.03)
    except Exception as e:
        yield f"Error: {e}"


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

llm = GeminiLLM(
    api_key="AIzaSyC__4SYJyttUSRsszBXAscUULwfDbiv84M",
    model="gemini-2.5-flash",
    temperature=0.0
)



SYSTEM_INTENT_CHECK = (
    "Does this user question NOT require retrieval from the documents or knowledge base (for example, if it is a greeting, thank you, or meta-question)? Reply ONLY with YES or NO."
)
SYSTEM_MARKDOWN = (
    "You are an AI assistant. Always format your answers using Markdown."
)

qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(search_kwargs={"k": 4}))
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')


# Streaming endpoint
@app.route('/ask', methods=['POST'])
def ask():
    global chat_history
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Let GeminiLLM decide if this is a simple greeting/thanks/meta-question
    intent_prompt = f"{SYSTEM_INTENT_CHECK}\nUser: {question}"
    intent_response = llm._call(intent_prompt).strip().upper()
    if intent_response == "YES":
        # Use Gemini streaming for simple conversation/meta-questions
        answer_prompt = f"{SYSTEM_MARKDOWN}\nUser: {question}"
        return Response(stream_gemini_response(answer_prompt), mimetype='text/plain')
    else:
        # Use RAG for everything else, but stream the answer word by word
        def stream_rag_answer():
            result = qa_chain({'question': question, 'chat_history': chat_history})
            answer = result['answer']
            chat_history.append((question, answer))
            nonlocal_answer = answer
            words = nonlocal_answer.split()
            for word in words:
                yield word + ' '
                time.sleep(0.03)
        return Response(stream_rag_answer(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
