# bot_logic.py
import re
from health_data import HEALTH_RULES, DEFAULT_RESPONSE

def preprocess_text(text):
    # Convert to lowercase and remove special characters
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def get_bot_response(user_message):
    cleaned_message = preprocess_text(user_message)
    
    # Loop through our rules to find a keyword match
    for intent, data in HEALTH_RULES.items():
        for keyword in data["keywords"]:
            if keyword in cleaned_message:
                return data["response"]
                
    return DEFAULT_RESPONSE
