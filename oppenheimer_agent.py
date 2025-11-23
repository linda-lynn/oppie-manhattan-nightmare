import os
import sys
from typing import List, Dict, Any
import ollama

class OppenheimerAgent:
    def __init__(self):
        self.name = "Oppenheimer AI"
        self.version = "1.0.0"
        self.model = "mistral"
        self.system_prompt = """You are an AI assistant named Oppenheimer, inspired by the famous physicist J. Robert Oppenheimer. 
        You are knowledgeable, thoughtful, and speak with a mix of scientific precision and philosophical depth. 
        You should respond to questions with both technical accuracy and human understanding."""
    
    def process_input(self, input_text: str) -> str:
        """Process the input using Ollama's Mistral model and return a response."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': self.system_prompt
                    },
                    {
                        'role': 'user',
                        'content': input_text
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error processing input: {str(e)}"

def main():
    agent = OppenheimerAgent()
    print(f"Starting {agent.name} v{agent.version}")
    print("Using Mistral model via Ollama")
    print("Type 'exit' or 'quit' to end the conversation")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            response = agent.process_input(user_input)
            print(f"Oppenheimer: {response}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 