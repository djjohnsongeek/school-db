from flask import flash
from app.models.enums import MessageCategory

def flash_message(message: str, category: MessageCategory):
    flash_cat = ""

    if category is MessageCategory.Success:
        flash_cat = "is-success"
    elif category is MessageCategory.Warn:
        flash_cat = "is-warning"
    elif category is MessageCategory.Error:
        flash_cat = "is-danger"
    else:
        flash_cat = ""

    flash(message, flash_cat)

def flash_messages(messages: [], category: MessageCategory):
    for m in messages:
        flash_message(m, category)