import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from ollama import Client

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Web Assistant", 
    page_icon="🧠", 
    layout="wide"
)

@st.cache_resource
def get_ollama_client():
    """Initialize Ollama client with API key from environment."""
    api_key = os.getenv('OLLAMA_API_KEY')
    if not api_key:
        st.error("Please set OLLAMA_API_KEY in your .env file")
        st.stop()
    
    return Client(
        headers={'Authorization': f'Bearer {api_key}'}
    )

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_available_tools(enable_web_search):
    """Get available tools based on settings."""
    client = get_ollama_client()
    if enable_web_search:
        return [client.web_search, client.web_fetch]
    else:
        return []

def display_chat_history(show_thinking):
    """Display the chat history."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                if "thinking" in message and message["thinking"] and show_thinking:
                    with st.expander("🤔 AI Thinking Process"):
                        st.write(message["thinking"])
                st.write(message["content"])

def process_ai_response(user_input, enable_web_search, show_thinking):
    """Process user input and get AI response."""
    
    # Add system message with current date/time context
    current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    system_message = {
        "role": "system", 
        "content": f"Current date and time: {current_time}. When users ask for 'latest', 'recent', 'today', or 'current' information, use web search with appropriate date context."
    }
    
    # Prepare messages for API (system message + conversation history)
    api_messages = [system_message] + [{"role": msg["role"], "content": msg["content"]} 
                                      for msg in st.session_state.messages]
    
    tools = get_available_tools(enable_web_search)
    client = get_ollama_client()
    
    try:
        with st.spinner("🤖 AI is thinking..."):
            response = client.chat(
                model='qwen3:4b',
                messages=api_messages,
                tools=tools,
                think=show_thinking
            )
        
        # Build assistant response
        assistant_message = {"role": "assistant", "content": response.message.content or ""}
        
        # Add thinking if available and enabled
        if response.message.thinking and show_thinking:
            assistant_message["thinking"] = response.message.thinking
        
        # Handle tool calls
        if response.message.tool_calls:
            tool_results = []
            with st.spinner("🔍 Using web tools..."):
                for tool_call in response.message.tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = getattr(client, function_name, None)
                    
                    if function_to_call:
                        try:
                            result = function_to_call(**tool_call.function.arguments)
                            # Format the result better and show more content
                            result_str = str(result)
                            if len(result_str) > 2000:
                                formatted_result = f"**{function_name}**:\n{result_str[:2000]}...\n\n*[Result truncated - showing first 2000 characters]*"
                            else:
                                formatted_result = f"**{function_name}**:\n{result_str}"
                            tool_results.append(formatted_result)
                        except Exception as e:
                            tool_results.append(f"**{function_name} Error**: {str(e)}")
            
            if tool_results:
                assistant_message["content"] += "\n\n---\n\n**🔍 Tool Results:**\n\n" + "\n\n---\n\n".join(tool_results)
        
        # Display the AI response immediately
        if "thinking" in assistant_message and assistant_message["thinking"] and show_thinking:
            with st.expander("🤔 AI Thinking Process"):
                st.write(assistant_message["thinking"])
        st.write(assistant_message["content"])
        
        st.session_state.messages.append(assistant_message)
        
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")

def main():
    """Main Streamlit app."""
    # Initialize session state
    initialize_session_state()
    
    # Sidebar controls
    with st.sidebar:
        st.title("🧠 AI Web Assistant")
        st.caption("Powered by AI with web search capabilities")
        
        # Model info
        st.info("**Model**: qwen3:4b")
        
        # Current time display
        current_time = datetime.now().strftime("%A, %B %d, %Y\n%I:%M %p")
        st.success(f"**Current Time:**\n{current_time}")
        
        # Toggles
        enable_web_search = st.toggle(
            "🌐 Enable Web Search", 
            value=True,
            help="Allow the AI to search the web for current information"
        )
        
        show_thinking = st.toggle(
            "🤔 Show AI Thinking", 
            value=False,
            help="Display the AI's reasoning process"
        )
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        # Chat stats
        st.caption(f"Messages: {len(st.session_state.messages)}")
        
        # Footer with LinkedIn link
        st.divider()
        st.markdown(
            """
            <div style='text-align: center; margin-top: 20px;'>
                <small>Built by <a href='https://www.linkedin.com/in/lesteroliver/' target='_blank' style='text-decoration: none; color: #0077B5;'>lesteroliver</a></small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Display chat history
    display_chat_history(show_thinking)
    
    # Chat input
    if user_input := st.chat_input("Ask me anything..."):
        # Add user message immediately and display it
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show user message right away
        with st.chat_message("user"):
            st.write(user_input)
        
        # Process AI response
        with st.chat_message("assistant"):
            process_ai_response(user_input, enable_web_search, show_thinking)
        
        st.rerun()

if __name__ == "__main__":
    main()
