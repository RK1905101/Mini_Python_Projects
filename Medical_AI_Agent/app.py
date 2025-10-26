from dotenv import load_dotenv
import streamlit as st
from RAG import get_medical_data, get_text_chunks, get_vectorstore, get_conversation_chain

def main():
    load_dotenv()

    st.set_page_config(page_title="Medical AI Agent", page_icon=":robot:")

    st.header(" 🩺  Medical AI Agent")

    # Initialize session state key, but set to None initially
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    # User input
    user_question = st.text_input("Enter your symptoms:")

    # Generate RAG pipeline when button clicked
    if st.button("Get Answer"):
        with st.spinner("Processing..."):
            raw_text = get_medical_data()
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            st.session_state.conversation = get_conversation_chain(vectorstore)
        st.success("Medical AI Agent is ready!")

    # Respond only if chain is ready
    if user_question:
        if st.session_state.conversation is not None:
            response = st.session_state.conversation.invoke( user_question)
            st.write(response["output"] if isinstance(response, dict) else response)
        else:
            st.warning("⚠️ Please click 'Get Answer' first to initialize the model.")

if __name__ == "__main__":
    main()
