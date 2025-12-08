import requests
import json

def correct_text_with_local_llm(text_to_correct: str, model_name: str = "llama3", ollama_url: str = "http://localhost:11434/api/generate") -> str:
    """
    Uses a locally running LLM via Ollama to correct text.

    Args:
        text_to_correct (str): The raw text with potential errors.
        model_name (str): The name of the model hosted by Ollama (e.g., 'llama3').
        ollama_url (str): The URL of the Ollama API endpoint.

    Returns:
        str: The corrected text.
    """
    prompt = f"""
    You are a text correction system. Your task is to fix common spelling and ordering errors in a short text.
    Given the input string, return only the most probable corrected output, without any extra explanation.

    Example 1:
    Input: "HELOLO WRLD"
    Output: "HELLO WORLD"

    Example 2:
    Input: "tetsng framewrok"
    Output: "TESTING FRAMEWORK"

    Input: "{text_to_correct}"
    Output:
    """

    try:
        response = requests.post(
            ollama_url,
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        print("Please ensure Ollama is running and the model '{model_name}' is installed ('ollama pull {model_name}').")
        # Fallback to returning the original text if the local LLM fails
        return text_to_correct