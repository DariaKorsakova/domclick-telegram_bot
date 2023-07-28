from aiogram.dispatcher import FSMContext

from main import bot, dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from keyboards import make_inline_kb_with_answers
from aiogram.dispatcher.filters.state import StatesGroup, State

HELP_COMMAND = """
/help - список команд;
/start - начать работу;
/description - описание бота;
"""


class UserState(StatesGroup):
    request = State()
    ask_sum_of_credit = State()
    sum_of_creedit = State()
    answer = State()
    ask_first_sum = State()
    first_sum = State()


async def send_to_admin(_):
    mess = 'Бот запущен'
    print(mess)


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.reply(HELP_COMMAND)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    markup = make_inline_kb_with_answers()
    await message.answer(text=f'Добрый день, <b>{message.from_user.first_name} {message.from_user.last_name}!</b>'
                              f'\nВозьмёшь ипотеку?:)', parse_mode='html', reply_markup=markup)

    await message.delete()


@dp.message_handler(commands=['description'])
async def description_command(message: Message):
    await message.answer(
        text="Привет! Я бот, который демонстрирует подачу завку на ипотеку в domclick")
    await message.delete()

@dp.callback_query_handler(state='*')
async def callback(callback: CallbackQuery, state: FSMContext): 
    if callback.data == 'Да, безусловно':
        async with state.proxy() as dat:
            dat["ask_sum_of_credit"] = True
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text="Введите запрашиваемую сумму кредита:")
    else:
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text="Возвращайтесь к нам!")

   
@dp.message_handler(state='*')
async def get_user_text(message: Message, state: FSMContext):
    async with state.proxy() as dat:
        dat["answer"] = message.text
    state_data = await state.get_data()
    answer = state_data.get('answer')
    asked_sum_of_credit = state_data.get('ask_sum_of_credit')
    asked_first_sum = state_data.get('ask_first_sum')
    sum_of_credit = state_data.get('sum_of_credit')
    if message.chat.type == 'private':
        try:
            if asked_sum_of_credit and float(answer):
                await message.answer("Введите сумму первоначального взноса: ",
                            parse_mode="html")
                async with state.proxy() as dat:
                    dat["ask_first_sum"] = True
                    dat["sum_of_credit"] = float(answer)
                    dat["ask_sum_of_credit"] = False
            elif asked_first_sum and float(answer):
                async with state.proxy() as dat:
                    dat["first_sum"] = float(answer)
                first_sum = float(answer)
                answer_to_reqs = checking_first_sum(sum_of_credit, first_sum)
                if answer_to_reqs:
                    await state.finish()
                    return await message.answer("Вы можете подать онлайн-заявку на ипотеку на сайте: https://domclick.ru/ipoteka/programs/onlajn-zayavka", parse_mode="html")
                else:
                    async with state.proxy() as dat:
                        dat["asked_sum_of_credit"] = True
                    return await message.answer("Необходимо указать бОльший первоначальный взнос", parse_mode="html")
        except ValueError:
            if answer.capitalize() in ['Привет', "Хай", "Доброе утро", "Добрый день", 'Добрый вечер']:
                mess = 'Добрый день ❤️'
            elif answer.capitalize() in ['Как дела?', "Как ты?"]:
                return await bot.send_sticker(message.from_user.id,
                                            sticker='CAACAgIAAxkBAAEFtv5jDa_q0t8Nr46yECvXuo7Id488zQACDQADwDZPE6T54fTUeI1TKQQ')
            else:
                mess = 'К сожалению, такого я еще не знаю!'
            await message.answer(mess, parse_mode='html')

def checking_first_sum(sum_of_credit, first_sum):
    if first_sum >= sum_of_credit * 0.15:
        return True
    else:
        return False

