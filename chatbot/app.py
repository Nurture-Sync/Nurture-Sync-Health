import streamlit as st
from streamlit_chat import message
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

def setup_chatbot():
    # Load PDF files from the directory
    loader = DirectoryLoader('chatbot/data/', glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(documents)

    # Create BioBERT embeddings for document retrieval
    embeddings = HuggingFaceEmbeddings(model_name="dmis-lab/biobert-base-cased-v1.2", model_kwargs={'device': "cpu"})

    # Initialize vector store with FAISS
    vector_store = FAISS.from_documents(text_chunks, embeddings)

    # Initialize memory to store conversation history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    st.title("SyncBot 👩🏻‍⚕")

    # Function to retrieve the most relevant text for the query
    def retrieve_answer(query):
        docs = vector_store.similarity_search(query, k=2)  # Retrieve top 2 relevant documents
        answer = "\n\n".join([doc.page_content for doc in docs])
        return answer

    def initialize_session_state():
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! You can ask me anything about Thyroid and diabetes 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

    def display_chat_history():
        reply_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Question:", placeholder="Ask about Thyroid and Diabetes", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = retrieve_answer(user_input)

                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with reply_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")

    # Initialize session state
    initialize_session_state()
    # Display chat history
    display_chat_history()

# Uncomment below line to test standalone
# if __name__ == "__main__":
#     setup_chatbot()
