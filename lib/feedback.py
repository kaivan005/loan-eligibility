from __future__ import annotations

from lib.mongo import (
    add_feedback as _add_feedback_mongo,
    get_feedback_for_user as _get_feedback_for_user_mongo,
    get_all_feedback as _get_all_feedback_mongo,
)


def add_feedback(user_email: str, user_name: str, rating: int, message: str) -> None:
    _add_feedback_mongo(
        user_email=user_email,
        user_name=user_name,
        rating=rating,
        message=message,
    )


def get_feedback_for_user(user_email: str) -> list[dict]:
    return _get_feedback_for_user_mongo(user_email)


def get_all_feedback() -> list[dict]:
    return _get_all_feedback_mongo()
