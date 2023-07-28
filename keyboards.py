from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

answers = {
    1: "Да, безусловно",
    2: "Еще нет"
}

def make_inline_kb_with_answers():
    markup = InlineKeyboardMarkup()
    btn_list = [InlineKeyboardButton(text=answers[x], callback_data=answers[x]) for x in range(1, 3)]
    markup.add(*btn_list)
    return markup



