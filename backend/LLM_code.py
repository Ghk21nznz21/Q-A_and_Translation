from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
from langchain.vectorstores import Chroma
import chromadb
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain.docstore.document import Document
import os 
from dotenv import load_dotenv
load_dotenv()

class VectorStore: 

    def __init__(self):
        self._apiKey =  os.getenv("OPENAI_API_KEY")
        self._startVectorStore()
        self.path = 'backend/files/'


        self.llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo", openai_api_key=self._apiKey)
            
    def _startVectorStore(self):
        self.client = chromadb.PersistentClient(path="files/chroma")
        embeddings = OpenAIEmbeddings(openai_api_key=self._apiKey)
        # Check if the collection already exists
        existing_collections = self.client.list_collections()
        collection_names = [collection.name for collection in existing_collections]
        if "RetrivalQA" not in collection_names:
            # Collection does not exist, so create it
            self.collection = self.client.create_collection(
                name="RetrivalQA",
                metadata={"hnsw:space": "cosine"},
                embedding_function=embeddings
            )
        else:
            # Collection already exists
            self.collection = self.client.get_collection("RetrivalQA")
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="RetrivalQA",
            embedding_function=embeddings,
        )
        
    def add_file(self, name: str, type: str, text: str):    
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
            splits = [Document(page_content=tx, metadata={'source': name, 'page': i, 'type': type}) 
                    for i, tx in enumerate(text_splitter.split_text(text.strip()))
            ]
            if splits:
                filtered_db = self.vectorstore.get(where={"source": name}) # size of list
                if filtered_db['ids']: #not empty 
                    return "Already Exists. Delete First"
                self.vectorstore.add_documents(splits)      
                return "Document Added"
            return "Nothing to add"
        except:
            return "Error Saving Document"
        
    def remove_file(self, path: str):
        docs = self.vectorstore.get(where={"source": path})
        self.vectorstore.delete(ids=docs['ids'])
        return 
    
    def translate(self, qa_output: str, language: str):
        print('Translating')
        completion = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful translator. Given an input text, translate it to the requested language. If there are any ambiguities, or things that couldn't be translated, please mention them after the translation.."},
            {"role": "user", "content": f"translate this content {qa_output} to {language}"}
          ]
        )
        print('Translating Response', completion.choices[0].message.content)
        return completion.choices[0].message.content

    def query(self, question: str, path: str, language: str):
        if path == "all":
            context_docs = self.vectorstore.as_retriever()
        else:
            context_docs = self.vectorstore.as_retriever(
                search_kwargs={"filter": {"source": path}})                 
        qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff", 
                retriever=context_docs,
                return_source_documents=True
        )
        # Make question and translate
        qa_output = qa_chain({"query": question}) # qa_chain.run(question) without return_source_documents
        print('Fetched from', qa_output['source_documents'])
        #self.translate(qa_output['result'], language)
        
        return qa_output # replace by translation when its working
        
if __name__ == "__main__":   
    vec = VectorStore()
    vec.add_file('gi.txt', 'txt', 'hi my old friend')
    vec.remove_file('gi.txt')
    vec.query('what does PDF mean', path='gi.txt') 
