import re
from datetime import datetime


MESSAGE_PATTERN = re.compile(
    r"^\s*[\u200e\u200f\u202a-\u202e\u2060\u2066\u2067]*"
    r"\[(\d{2}/\d{2}/\d{2}),\s+"
    r"(\d{1,2}:\d{2}:\d{2}\s*[AP]M)\]\s+"
    r"(.*)$"
)


def parse_whatsapp_chat(file_path: str):
    messages = []

    with open(file_path, "r", encoding="utf-8-sig") as file:
        lines = file.readlines()

    current_message = None

    for line in lines:
        line = line.rstrip("\n")

        match = MESSAGE_PATTERN.match(line)

        if match:
            date_str, time_str, content = match.groups()

            timestamp = datetime.strptime(
                f"{date_str} {time_str}",
                "%d/%m/%y %I:%M:%S %p"
            )

            if ": " in content:
                sender, message_text = content.split(": ", 1)

                sender = sender.strip()
                message_text = message_text.strip()

                # WhatsApp system messages
                if (
                    sender == "Final Year Project🚀"
                    and (
                        "Messages and calls are end-to-end encrypted" in message_text
                        or "You created group" in message_text
                    )
                ):
                    current_message = {
                        "timestamp": timestamp,
                        "sender": None,
                        "message": message_text,
                        "type": "system"
                    }

                else:
                    current_message = {
                        "timestamp": timestamp,
                        "sender": sender,
                        "message": message_text,
                        "type": "message"
                    }

            else:
                current_message = {
                    "timestamp": timestamp,
                    "sender": None,
                    "message": content.strip(),
                    "type": "system"
                }

            messages.append(current_message)

        else:
            # Continuation of a multiline message
            if current_message and line.strip():
                current_message["message"] += "\n" + line.strip()

    return messages