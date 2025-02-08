import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiChat:
    def __init__(self):
        # Set up Gemini configuration
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")  # Use appropriate Gemini model

    # def generate_response(self, user_message, chat_history=None):
    #     try:
    #         if chat_history is None:
    #             chat_history = []
    #
    #         # Construct chat context
    #         chat_history.append({"role": "user", "content": user_message})
    #         response = self.model.generate_content(user_message, context=chat_history)
    #
    #         chat_history.append({"role": "model", "content": response.text})
    #         return response.text
    #     except Exception as e:
    #         return f"Error generating response: {str(e)}"def generate_response(self, user_message, chat_history=None):

    def generate_response(self, user_message, chat_history=None):
        try:
            if chat_history is None:
                chat_history = []

            # Construct prompt with chat history context
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            prompt += f"\nuser: {user_message}"

            # Generate response without the 'context' parameter
            response = self.model.generate_content(prompt)

            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
