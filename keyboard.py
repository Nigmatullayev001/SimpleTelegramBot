from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_template_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Green", callback_data="tpl_green"),
                InlineKeyboardButton(text="🔵 Blue", callback_data="tpl_blue"),
            ],
            [
                InlineKeyboardButton(text="💖 Pink", callback_data="tpl_pink"),
                InlineKeyboardButton(text="⬛ Black-Green", callback_data="tpl_black_green"),
            ]
        ]
    )


def get_format_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 PDF", callback_data="save_pdf"),
                InlineKeyboardButton(text="📝 Word", callback_data="save_docx"),
                InlineKeyboardButton(text="📊 PowerPoint", callback_data="save_pptx"),
            ]
        ]
    )


def save_request():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏁 Tugatish", callback_data="finish")],
            [InlineKeyboardButton(text="🗑 Tozalash", callback_data="clear")]
        ]
    )


def custom_text_size():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔠 Kichik 14", callback_data="text_14"),
                InlineKeyboardButton(text="🔠 O‘rta 18", callback_data="text_18"),
                InlineKeyboardButton(text="🔠 Katta 24", callback_data="text_24"),
            ]
        ]
    )


def custom_page_split():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 element = 1 varoq", callback_data="page_1"),
            ],
            [
                InlineKeyboardButton(text="2 element = 1 varoq", callback_data="page_2"),
            ],
            [
                InlineKeyboardButton(text="3 element = 1 varoq", callback_data="page_3"),
            ]
        ]
    )
