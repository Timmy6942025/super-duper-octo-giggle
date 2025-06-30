# main.py
import os
from flask import Flask, request, jsonify, render_template
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from gemini_llm import GeminiLLM

app = Flask(__name__)


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

llm = GeminiLLM(
    api_key="AIzaSyC__4SYJyttUSRsszBXAscUULwfDbiv84M",
    model="gemini-2.5-flash
    ",
    temperature=0.0
)
qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(search_kwargs={"k": 4}))
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global chat_history
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    result = qa_chain({'question': question, 'chat_history': chat_history})
    answer = result['answer']
    chat_history.append((question, answer))
    chat_history = chat_history[-10:]
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
