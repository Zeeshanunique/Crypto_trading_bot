# main.py

import streamlit as st
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
from huggingface_hub import login, HfFolder
import torch
import gc
import os
from pathlib import Path

# Suppress symlinks warning
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Constants
MAX_LENGTH = 32768
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "agarkovv/CryptoTrader-LM"
BASE_MODEL_ID = "mistralai/Ministral-8B-Instruct-2410"
CACHE_DIR = Path.home() / ".cache" / "huggingface"

def init_huggingface_auth():
    hf_token = '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' 
    if not hf_token:
        with st.sidebar:
            hf_token = st.text_input(
                "Enter Hugging Face Token:",
                type="password",
                help="Get your token from https://huggingface.co/settings/tokens"
            )
    
    if hf_token:
        try:
            login(token=hf_token)
            return True
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False
    return False

@st.cache_resource
def load_model():
    try:
        if not HfFolder.get_token():
            st.error("Please provide a valid Hugging Face token")
            return None, None
            
        progress_text = "Loading model..."
        progress_bar = st.progress(0)
        
        progress_bar.progress(25)
        tokenizer = AutoTokenizer.from_pretrained(
            BASE_MODEL_ID,
            cache_dir=CACHE_DIR,
            use_auth_token=True
        )
        
        progress_bar.progress(50)
        model = AutoPeftModelForCausalLM.from_pretrained(
            MODEL_ID,
            cache_dir=CACHE_DIR,
            use_auth_token=True,
            torch_dtype=torch.float32
        )
        
        progress_bar.progress(75)
        model = model.to(DEVICE)
        model.eval()
        
        progress_bar.progress(100)
        return model, tokenizer
        
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None
    finally:
        if 'progress_bar' in locals():
            progress_bar.empty()

def generate_response(prompt, model, tokenizer):
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        inputs = tokenizer(
            f"[INST]{prompt}[/INST]",
            return_tensors="pt",
            padding=False,
            max_length=MAX_LENGTH,
            truncation=True
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            output = model.generate(
                **inputs,
                use_cache=True,
                max_new_tokens=MAX_LENGTH,
            )
            
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response
        
    except Exception as e:
        return f"Error generating response: {str(e)}"
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = None
    if "tokenizer" not in st.session_state:
        st.session_state.tokenizer = None

def main():
    st.set_page_config(
        page_title="CryptoTrader AI Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("CryptoTrader AI Assistant")
    initialize_session_state()
    
    if not init_huggingface_auth():
        st.warning("Please provide your Hugging Face token to continue")
        return
        
    if not st.session_state.model:
        st.session_state.model, st.session_state.tokenizer = load_model()
    
    if not st.session_state.model or not st.session_state.tokenizer:
        return
        
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask about cryptocurrency trading..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = generate_response(
                prompt,
                st.session_state.model,
                st.session_state.tokenizer
            )
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()