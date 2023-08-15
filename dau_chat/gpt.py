from flask import Flask, render_template, request, redirect, url_for
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

app = Flask(__name__)


os.environ["OPENAI_API_KEY"] = "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"

loader = DirectoryLoader('./info', glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

persist_directory = 'db'
embedding = OpenAIEmbeddings()

vectordb = Chroma.from_documents(
    documents=texts,
    embedding=embedding,
    persist_directory=persist_directory)

vectordb.persist()
retriever = vectordb.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True)

def process_llm_response(llm_response):
    result = llm_response['result']
    sources = [source.metadata['source'] for source in llm_response["source_documents"]]
    return result, sources


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']
    llm_response = qa_chain(query)
    result, sources = process_llm_response(llm_response)
    return render_template('index.html', result=result, sources=sources)

@app.route('/add_info')
def add_info():
    return render_template('add_info.html')

@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    data = request.form['data']  # 클라이언트로부터 전송된 데이터

    with open('./info/user_data.txt', 'r', encoding="cp949") as file:
        existing_data = file.read()

    with open('./info/user_data.txt', 'w', encoding="cp949") as file:
        combined_data = existing_data + '\n' + data
        file.write(combined_data)

    return redirect(url_for('save_complete'))

@app.route('/save_complete')
def save_complete():
    return '''
        <script>
            alert("저장완료");
            window.location.href = "/";
        </script>
    '''

if __name__ == '__main__':
    app.run(debug=True)
