# Gym Assistant Chatbot

A conversational AI assistant that helps with gym-related queries, workout advice, and nutrition guidance based on the Fit4Life Academy approach.

## Features

- Personalized fitness and nutrition advice
- Workout recommendations
- Weight loss and muscle building guidance
- Conversational, human-like responses
- Simple and intuitive chat interface

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Groq API key (sign up at https://console.groq.com to get one)

### Installation

1. Clone or download this repository

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Running the Application

Start the Streamlit app with:

```
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

1. Type your fitness-related question in the chat input box
2. Receive personalized advice based on your query
3. Continue the conversation with follow-up questions
4. Use the "Clear Chat" button in the sidebar to start a new conversation

## About

This chatbot uses the Groq LLama3-70B model to generate human-like responses to fitness queries. The knowledge base is derived from Fit4Life Academy's approach to sustainable fitness and health transformation.

## Note

This assistant provides general fitness information and is not a substitute for professional medical advice.
