import streamlit as st
import ollama
import time
import uuid
import json
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Ensure chat history directory exists
CHAT_HISTORY_DIR = "chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)


def create_chat(message, role):
    """
    Create a dictionary representation of a chat message
    """
    return {"role": role, "content": message}


def get_chat_response(model, temperature, messages):
    """
    Get streaming response from Ollama
    """
    return ollama.chat(
        messages=messages,
        stream=True,
        model=model,
        options={"temperature": temperature},
    )


def save_chat_history(chat_history, username, chat_name=None):
    """
    Save current chat history to a file with username
    """
    if not chat_name:
        chat_name = f"chat_{str(uuid.uuid4())[:8]}"

    # Include username in the chat data
    chat_data = {"owner": username, "messages": chat_history}

    filename = os.path.join(CHAT_HISTORY_DIR, f"{chat_name}.json")
    with open(filename, "w") as f:
        json.dump(chat_data, f)
    return chat_name


def load_chat_history(filename):
    """
    Load a specific chat history
    """
    with open(os.path.join(CHAT_HISTORY_DIR, filename), "r") as f:
        return json.load(f)


def get_saved_chats(username):
    """
    Retrieve list of saved chat filenames for specific user
    """
    all_chats = [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith(".json")]
    user_chats = []

    for chat_file in all_chats:
        chat_data = load_chat_history(chat_file)
        if chat_data.get("owner") == username:
            user_chats.append(chat_file)

    return user_chats


def load_credentials():
    """
    Load user credentials from a YAML file
    """
    with open("users/user.yml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def authenticate():
    config = load_credentials()

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator


def new_chat(username):
    if "chat_history" in st.session_state and st.session_state["chat_history"]:
        saved_name = save_chat_history(st.session_state["chat_history"], username)
        st.success(f"Current chat saved as {saved_name}")

    st.session_state["chat_history"] = []
    st.rerun()
    return None


def delete_chat(chat_to_delete, username):
    try:
        chat_data = load_chat_history(chat_to_delete)
        if chat_data.get("owner") == username:
            os.remove(os.path.join(CHAT_HISTORY_DIR, chat_to_delete))
            st.success(f"Chat {chat_to_delete} deleted successfully")
            st.rerun()
        else:
            st.error("You don't have permission to delete this chat")
    except Exception as e:
        st.error(f"Error deleting chat: {e}")


def chat(prompt, model_choice, temperature):
    st.session_state["chat_history"].append(create_chat(prompt, "user"))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = ""
        response_stream = st.empty()
        try:
            for chunk in get_chat_response(
                model_choice, temperature, st.session_state["chat_history"]
            ):
                response += chunk["message"]["content"] + " "
                response_stream.markdown(response)
                time.sleep(0.05)
            response_stream.markdown(response)
            st.session_state["chat_history"].append(create_chat(response, "assistant"))
        except Exception as e:
            st.error(f"Error occurred: {e}")


def main():
    """
    The main function of the secure Ollama chatbot with chat history.
    This function handles user authentication, chat management, and chat functionality.
    """
    st.title("Secure Ollama Chatbot with Chat History")
    authenticator = authenticate()
    name, authentication_status, username = authenticator.login("main")

    if authentication_status:
        st.write(f"Welcome *{name}*")

        with st.sidebar:
            st.subheader("Chat Management")

            model_choice = st.selectbox("Choose a model", ["llama3.2", "llama3.1"])
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7)

            if st.button("Start New Chat"):
                new_chat(username)

            st.subheader("Your Saved Chats")
            saved_chats = get_saved_chats(username)
            selected_chat = st.selectbox(
                "Load a previous chat",
                [""] + saved_chats,
                format_func=lambda x: x.replace(".json", "") if x else "",
            )
            if selected_chat:
                try:
                    loaded_chat = load_chat_history(selected_chat)
                    if st.button("Load Chat"):
                        st.session_state["chat_history"] = loaded_chat["messages"]
                        st.rerun()
                except Exception as e:
                    st.error(f"Error loading chat: {e}")
            if saved_chats:
                chat_to_delete = st.selectbox(
                    "Delete a saved chat",
                    [""] + saved_chats,
                    key="delete_chat",
                    format_func=lambda x: x.replace(".json", "") if x else "",
                )
                if chat_to_delete and st.button("Delete Selected Chat"):
                    delete_chat(chat_to_delete, username)

            authenticator.logout("Logout", location="sidebar")
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        prompt = st.chat_input("Enter your message")
        if prompt:
            chat(prompt, model_choice, temperature)

    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")


if __name__ == "__main__":
    main()
