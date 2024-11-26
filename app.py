# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from agents import AgentManager
from utils.logger import logger

# Must be the first Streamlit command
st.set_page_config(
    page_title="Crypto AI Agent System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS styling
def load_css():
    st.markdown("""
        <style>
        .main { padding: 2rem; }
        .stSelectbox { margin-bottom: 2rem; }
        .task-description {
            padding: 1rem;
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Header with logo/description
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 Crypto AI System")
        st.markdown("*Your intelligent crypto assistant for chatting, predicting, and analyzing*")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Task selection with descriptions
    task_descriptions = {
        "Crypto Chatbot": "Chat with an AI about cryptocurrency topics, market trends, and technical analysis",
        "Price Prediction": "Get AI-powered price predictions for various cryptocurrencies",
        "Summarize Cryptocurrency Articles": "Get quick summaries of crypto news and articles",
        "Crypto Education Tool": "Learn about cryptocurrency concepts and terminology"
    }
    
    selected_task = st.sidebar.selectbox(
        "Choose a task:",
        list(task_descriptions.keys())
    )
    
    # Show task description
    with st.sidebar.expander("About this task"):
        st.write(task_descriptions[selected_task])
    
    # Main content area
    with st.container():
        st.markdown(f"### {selected_task}")
        st.markdown(f"*{task_descriptions[selected_task]}*")
        
        try:
            agent_manager = AgentManager()
            
            if selected_task == "Crypto Chatbot":
                chatbot_section(agent_manager)
            elif selected_task == "Price Prediction":
                prediction_section(agent_manager)
            elif selected_task == "Summarize Cryptocurrency Articles":
                summarize_section(agent_manager)
            elif selected_task == "Crypto Education Tool":
                education_section(agent_manager)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Error in main app: {str(e)}")

def chatbot_section(agent_manager):
    st.header("Crypto Chatbot")

    # Initialize session state for message history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input at the bottom
    if prompt := st.chat_input("What would you like to know about cryptocurrencies?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chatbot response
        chatbot_agent = agent_manager.get_agent("chatbot")
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            try:
                for response in chatbot_agent.execute(prompt):
                    full_response += response
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Error: {e}")
                logger.error(f"ChatbotAgent Error: {e}")

    # Add a clear button to reset the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

def prediction_section(agent_manager):
    st.header("Price Prediction")

    # Predefined list of currencies with horizontal buttons
    coin = None
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        if st.button("BTC"):
            coin = "BTC"
    with col2:
        if st.button("ETH"):
            coin = "ETH"
    with col3:
        if st.button("USDT"):
            coin = "USDT"
    with col4:
        if st.button("BNB"):
            coin = "BNB"

    # Manual input option
    manual_coin = st.text_input("Or enter the cryptocurrency symbol manually (e.g., BTC, ETH):")
    if manual_coin:
        coin = manual_coin.lower()

    if coin:
        predictor_agent = agent_manager.get_agent("predictor")
        with st.spinner("Predicting..."):
            try:
                prediction = predictor_agent.execute(coin)
                st.subheader("Prediction:")
                st.write(prediction)
            except Exception as e:
                st.error(f"Error: {e}")
                logger.error(f"PredictorAgent Error: {e}")

def summarize_section(agent_manager):
    st.header("Summarize Cryptocurrency Articles")
    text = st.text_area("Enter cryptocurrency-related text to summarize:", height=200)
    if st.button("Summarize"):
        if text:
            main_agent = agent_manager.get_agent("summarize")
            validator_agent = agent_manager.get_agent("summarize_validator")
            with st.spinner("Summarizing..."):
                try:
                    summary = main_agent.execute(text)
                    st.subheader("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SummarizeAgent Error: {e}")
                    return

            with st.spinner("Validating summary..."):
                try:
                    validation = validator_agent.execute(original_text=text, summary=summary)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SummarizeValidatorAgent Error: {e}")
        else:
            st.warning("Please enter text to summarize.")

def education_section(agent_manager):
    st.header("Crypto Education Tool")
    topic = st.text_input("Enter a topic to learn about cryptocurrencies:")
    if st.button("Learn"):
        if topic:
            education_agent = agent_manager.get_agent("education_tool")
            with st.spinner("Learning..."):
                try:
                    response = education_agent.execute(topic)
                    st.subheader("Response:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"EducationAgent Error: {e}")
        else:
            st.warning("Please enter a topic to learn about.")

if __name__ == "__main__":
    main()