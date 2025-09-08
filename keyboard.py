from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤖 Avtomatik", callback_data="mode_auto")],
            [InlineKeyboardButton(text="⚙️ Maxsus", callback_data="mode_custom")]
        ]
    )
    return kb


def get_format_keyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 PDF", callback_data="save_pdf"),
                InlineKeyboardButton(text="📝 Word", callback_data="save_docx"),
                InlineKeyboardButton(text="📊 PowerPoint", callback_data="save_pptx"),
            ]
        ]
    )
    return kb


def save_request():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏁 Tugatish", callback_data="finish")]
        ]
    )
    return kb


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


def custom_image_size():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼️ Kichik", callback_data="img_small"),
                InlineKeyboardButton(text="🖼️ O‘rta", callback_data="img_medium"),
                InlineKeyboardButton(text="🖼️ Katta", callback_data="img_large"),
            ]
        ]
    )


def custom_page_split():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 varoq = 1 element", callback_data="page_1"),
            ],
            [
                InlineKeyboardButton(text="1 varoq = 2 element", callback_data="page_2"),
            ],
            [
                InlineKeyboardButton(text="1 varoq = 3 element", callback_data="page_3"),
            ]
        ]
    )
