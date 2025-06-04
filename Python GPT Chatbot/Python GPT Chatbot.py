# Import the OpenAI library to interact with the OpenAI API
import openai

# Set the API key to authenticate with OpenAI's servers
# Instead, use environment variables or a configuration file.
openai.api_key = "Get your API Key from https://platform.openai.com/api-keys"

# Function to interact with OpenAI's ChatGPT model
def chat_with_gpt(chat_log):
    # Send the conversation history to the OpenAI API and get a response
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', # Specify the model to use
                                            messages=chat_log # Pass the conversation history
                                          )
    # Extract and return the assistant's reply from the response
    return response.choices[0].message.content.strip()

# Initialize an empty chat history
chat_log = []

# Define the number of messages to remember in the conversation
n_remembered_post = 2


# Main loop to interact with the chatbot
if __name__ == "__main__":
    while True:
        # Take user input from the console
        user_input = input("You: ")
        # Exit the loop if the user types 'quit', 'exit', or 'bye'
        if user_input.lower() in ['quit', "exit", "bye"]:
            break
        
        # Add the user's message to the chat history
        chat_log.append({'role': 'user', 'content': user_input})
        
        # Limit the chat history to only the last `n_remembered_post` messages
        if len(chat_log) > n_remembered_post:
            del chat_log[:len(chat_log)-n_remembered_post] # Remove older messages

        # Get the chatbot's response
        response = chat_with_gpt(chat_log)
        
        # Print the chatbot's response to the console
        print("Chatbot:", response)
        
        # Add the chatbot's response to the chat history
        chat_log.append({'role': "assistant", 'content': response})