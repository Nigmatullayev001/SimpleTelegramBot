from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_template_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Green", callback_data="template_green")],
        [InlineKeyboardButton(text="🔵 Blue", callback_data="template_blue")],
        [InlineKeyboardButton(text="💜 Pink", callback_data="template_pink")]
    ])


def get_finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏁 Tugatish", callback_data="finish"),
            InlineKeyboardButton(text="📝 Faqat matn", callback_data="only_text"),
        ]
    ])


def get_format_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 PDF", callback_data="format_pdf")],
        [InlineKeyboardButton(text="🧾 DOCX", callback_data="format_docx")],
        [InlineKeyboardButton(text="🎞 PPTX", callback_data="format_pptx")],
    ])
