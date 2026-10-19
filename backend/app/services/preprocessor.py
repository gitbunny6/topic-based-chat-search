import re


def clean_message(text: str) -> str:
    """
    Clean a WhatsApp message while keeping its meaning.
    """

    # Remove invisible Unicode formatting characters
    text = re.sub(r"[\u200e\u200f\u202a-\u202e\u2060\u2066\u2067]", "", text)

    # Remove WhatsApp media placeholder
    text = text.replace("image omitted", "")
    text = text.replace("video omitted", "")
    text = text.replace("audio omitted", "")
    text = text.replace("sticker omitted", "")

    # Remove edited-message marker
    text = text.replace("<This message was edited>", "")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_messages(messages: list) -> list:
    """
    Clean parsed WhatsApp messages and remove
    messages that are not useful for semantic search.
    """

    cleaned_messages = []

    for message in messages:

        # Ignore WhatsApp system messages
        if message["type"] == "system":
            continue

        cleaned_text = clean_message(message["message"])

        # Ignore messages that become empty after cleaning
        if not cleaned_text:
            continue

        cleaned_messages.append({
            "timestamp": message["timestamp"],
            "sender": message["sender"],
            "message": cleaned_text,
            "type": "message"
        })

    return cleaned_messages