# from core.constants import (
#     GREETINGS,
#     MAX_CHAT_HISTORY,
# )


# def is_greeting(query: str) -> bool:

#     normalized_query = (
#         query.lower().strip()
#     )

#     return normalized_query in GREETINGS


# def format_chat_history(
#     chat_history: list[dict],
#     limit: int = MAX_CHAT_HISTORY,
# ) -> str:

#     recent_messages = (
#         chat_history[-limit:]
#     )

#     return "\n".join(
#         (
#             f"{message['role']}: "
#             f"{message['content']}"
#         )
#         for message in recent_messages
#     )

from core.constants import (
    GREETINGS,
    MAX_CHAT_HISTORY,
)


def is_greeting(query: str) -> bool:
    return query.lower().strip() in GREETINGS


def format_chat_history(
    chat_history: list[dict],
    limit: int = MAX_CHAT_HISTORY,
) -> str:

    recent_messages = chat_history[-limit:]

    return "\n".join(
        f"{message['role']}: {message['content']}"
        for message in recent_messages
    )