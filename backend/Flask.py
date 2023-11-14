from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dataclasses import dataclass

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import chromadb
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain.docstore.document import Document
from LLM_code import VectorStore


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})


# Note: Currently data is shared beetween all users 
functionalities = VectorStore()

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    try:
        message = functionalities.add_file(data['name'], data['type'], data['text'])
        return jsonify({"message": message}), 200 
    except:
        return jsonify({"message": "Wrong Inputs"}), 400


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    print(data)
    try:
        question = data['text'] 
        language = data['language'] 
        task = data['task']
        if task == 'QA':
            fileName = data['fileName'] 
            qa_output = functionalities.query(question, fileName, language)
            response = {'message': qa_output}
        else: 
            # Translation
            # Perform translation using your functionality
            translation_output = functionalities.translate(question, language)
            response = {'message': translation_output}
        return jsonify(response), 200
    except: 
        return jsonify({"message": "Error"}), 400


if __name__ == '__main__':
    app.run(debug=True)


