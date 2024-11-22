# Secure Ollama Chatbot with Chat History

A Streamlit-based web application that provides a secure interface for interacting with Ollama models. The application features user authentication, chat history management, and customizable model parameters.

## Features

- 🔐 Secure user authentication
- 💬 Chat with Ollama models (llama3.1 and llama3.2)
- 📚 Save and load chat histories
- 🗑️ Delete previous chat sessions
- 🎛️ Adjustable model parameters (temperature)
- 👥 Multi-user support with isolated chat histories

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running on your system
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up user authentication:
   - Create a `users` directory
   - Create a `user.yml` file inside the `users` directory with the following structure:
```yaml
credentials:
  usernames:
    username1:
      email: user1@example.com
      name: User One
      password: <hashed-password>
cookie:
  expiry_days: 30
  key: random_signature_key
  name: random_cookie_name
```

## Usage

1. Start the Ollama service on your system

2. Run the Streamlit application:
```bash
streamlit run chat_llama.py
```

3. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

4. Log in using your credentials

5. Features available after login:
   - Select different Ollama models
   - Adjust temperature parameter
   - Start new chat sessions
   - Save current chat
   - Load previous chats
   - Delete saved chats
   - Log out

## Project Structure

```
.
├── chat_llama.py          # Main application file
├── requirements.txt       # Python dependencies
├── chat_histories/       # Directory for stored chat histories
├── users/               # Directory for user authentication
│   └── user.yml        # User credentials and settings
└── README.md           # This file
```

## Security Features

- Secure user authentication using `streamlit-authenticator`
- Password hashing for user credentials
- Isolated chat histories per user
- Session management with secure cookies

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

[Specify your license here]

## Notes

- Ensure Ollama is properly installed and running before starting the application
- Keep your `user.yml` file secure and never commit it to version control
- Regular backups of chat histories are recommended
- The application requires a stable internet connection for model interactions