import streamlit as st
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import ChatMessage
from dotenv import load_dotenv

load_dotenv()

# Function to load and parse the document
def load_document(file):
    content = file.read().decode("utf-8")
    return Document(text=content)

# Function to build the vector store and index
def build_index(documents):
    vector_index = VectorStoreIndex.from_documents(documents)
    return vector_index

# Streamlit app layout
st.title("Chat with Document")

# File uploader
uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True, type=["txt", "md"])

if uploaded_files:
    st.write("Processing documents... This might take a few moments.")
    documents = [load_document(file) for file in uploaded_files]
    index = build_index(documents)
    
    chat_store = SimpleChatStore()
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
    )

    chat_engine = index.as_chat_engine(
        chat_mode='context',
        memory=memory,
        system_prompt="You are a chatbot designed to answer questions based on the provided context. If a question falls outside of the given context, kindly inform the user that the question cannot be answered. Be short and concise.",
        streaming=True
    )

    st.success("Documents processed! Start chatting below.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(""):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = chat_engine.stream_chat(prompt, [
                ChatMessage(message['content'], role= message['role']) for message in st.session_state.messages
            ])
            
            st.write_stream(response.response_gen)
                
        st.session_state.messages.append({"role": "assistant", "content": response.response})

else:
    st.info("Please upload at least one document to start.")
