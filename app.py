import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Gym Assistant", page_icon="💪", layout="centered")

# Custom CSS for chat interface
st.markdown("""
<style>
.stTextInput > div > div > input {border-radius: 20px;}
.chat-message {padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: row;}
.chat-message.user {background-color: #2b313e;}
.chat-message.assistant {background-color: #475063;}
.chat-message .avatar {width: 20%;}
.chat-message .avatar img {max-width: 78px; max-height: 78px; border-radius: 50%; object-fit: cover;}
.chat-message .message {width: 80%; padding-left: 1rem;}
div.stButton > button:first-child {background-color: #4CAF50; color: white; border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")

# If running on Streamlit Cloud, try to get from st.secrets
if not groq_api_key and hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    
if not groq_api_key:
    st.error("GROQ API key not found. Please set it in .env file for local development or in Streamlit secrets for cloud deployment.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Fitness knowledge base from Fit4Life Academy
FITNESS_KNOWLEDGE = """
Fit4Life Academy helps people lose fat, build muscle, and transform their health with personalized, science-backed nutrition and fitness coaching.

Key offerings:
- Personalized fitness and nutrition plans
- Long-term sustainable approaches (not quick fixes)
- Body transformation coaching
- Weight loss and muscle building programs

Philosophy:
- 97% of people who lose weight regain it within five years
- Quick fixes don't address behaviors needed for long-term success
- Rigid rules and one-size-fits-all solutions don't work long-term
- Plans should fit your life, not the other way around

Approach:
- Science-backed methods
- Personalized programs based on individual goals and lifestyle
- Focus on sustainable habits rather than temporary diets
- Building a healthy relationship with food and exercise

Client results include:
- Fat loss while maintaining muscle
- Improved blood markers and overall health
- Increased strength and energy
- Better relationship with food and body image
- Long-term maintenance of results
"""

# App title
st.title("💪 Gym Assistant")
st.subheader("Your personal fitness coach powered by AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response
def generate_response(prompt):
    # Prepare messages with system prompt and chat history
    messages = [
        {"role": "system", "content": f"""You're a gym buddy texting fitness advice. Keep it SUPER casual and brief - like you're texting a friend.

KNOWLEDGE BASE:
Fit4Life approach: {FITNESS_KNOWLEDGE}

TEXT LIKE A HUMAN:
- Keep it SHORT. 1-3 sentences max per "text bubble"
- Use casual language like "yeah", "tbh", "honestly", "hey", "look"
- Drop words sometimes ("Going gym later?" not "Are you going to the gym later?")
- Use incomplete sentences occasionally
- Add filler words: "um", "like", "y'know", "honestly", "basically"
- Use contractions always (can't, don't, you're, we're, that's)
- Vary your openings ("So", "Well", "Hmm", "Look", "OK so")
- Add natural pauses with line breaks between thoughts
- Personalize based on what they just asked
- Keep responses under 50 words total when possible

AVOID COMPLETELY:
- Formal language or technical terms
- Long explanations
- Robotic/repetitive patterns
- Overloading with information
- Starting every message the same way

EXAMPLES:

User: "How do I lose belly fat?"
You: "Honestly? Spot reduction's a myth.

Best bet is eating better + moving more.

Mix cardio with strength training and watch portions. Small changes add up!"

User: "What's a good workout for beginners?"
You: "Keep it simple! Bodyweight stuff is perfect to start.

Try squats, push-ups (on knees if needed), and planks.

Consistency > intensity at first. 3x a week for 20-30 mins is plenty."

User: "I hate cardio, what should I do?"
You: "Yeah, cardio can be boring af.

Try something fun instead - dancing, hiking, basketball, whatever.

Or just lift weights with shorter rest periods. Gets your heart rate up too."

Remember: Text like a real person would text their friend!"""},
    ]
    
    # Add chat history
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add user's new message
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Get response from Groq
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Process streaming response
        response_text = ""
        response_placeholder = st.empty()
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            response_text += content
            response_placeholder.markdown(response_text)
        
        return response_text
    
    except Exception as e:
        return f"Sorry, I'm having trouble connecting right now. Error: {str(e)}"

# Accept user input
if prompt := st.chat_input("Ask me anything about fitness, workouts, or nutrition..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = generate_response(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with instructions
with st.sidebar:
    st.title("About this Assistant")
    st.markdown("""
    This gym assistant is powered by AI and provides guidance on:
    - Workout routines
    - Nutrition advice
    - Weight loss strategies
    - Muscle building tips
    - Fitness motivation
    
    Based on the Fit4Life Academy approach to fitness and health.
    
    **Note:** This assistant provides general fitness information and is not a substitute for professional medical advice.
    """)
    
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Type your fitness question in the chat box
    2. Get personalized advice based on your goals
    3. Ask follow-up questions for more details
    """)
    
    # Add a clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
