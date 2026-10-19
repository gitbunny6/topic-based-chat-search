def create_chunks(messages: list, max_characters: int = 500) -> list:
    """
    Combine consecutive messages into chunks of approximately
    max_characters characters.
    """

    chunks = []
    current_messages = []
    current_length = 0

    for message in messages:

        formatted_message = (
            f'{message["sender"]}: {message["message"]}'
        )

        message_length = len(formatted_message)

        # If adding this message would make the chunk too large,
        # save the current chunk first.
        if (
            current_messages
            and current_length + message_length > max_characters
        ):
            chunks.append(build_chunk(current_messages))

            current_messages = []
            current_length = 0

        current_messages.append(message)
        current_length += message_length

    # Add the final chunk
    if current_messages:
        chunks.append(build_chunk(current_messages))

    return chunks


def build_chunk(messages: list) -> dict:
    """
    Convert a group of messages into one searchable chunk.
    """

    text = "\n".join(
        f'{message["sender"]}: {message["message"]}'
        for message in messages
    )

    return {
        "text": text,
        "start_time": messages[0]["timestamp"],
        "end_time": messages[-1]["timestamp"],
        "message_count": len(messages)
    }