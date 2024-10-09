import logging
from modules import bot_logic, api
from aiogram import Bot, types, F, Dispatcher, Router
from aiogram.filters.command import Command
from aiogram.types.input_file import InputFile
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from middlewares.message_middleware import message_middleware
from middlewares.callback_middleware import callback_middleware
from middlewares.inline_middleware import inline_middleware

router = Router()

# Описание состояний для FSM
class VoucherStates(StatesGroup):
    waiting_for_voucher = State()

router.message.middleware(message_middleware())
router.callback_query.middleware(callback_middleware())
router.inline_query.middleware(inline_middleware())

#|=============================[Commands]=============================|
# Хэндлер на /start
@router.message(Command('start'))
async def start(message: types.Message):
    text, markup = await bot_logic.start_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на /menu
@router.message(Command('menu'))
async def menu(message: types.Message):
    text, markup = await bot_logic.menu_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на команду /voucher
@router.message(Command("voucher"))
async def start_voucher_process(message: Message, state: FSMContext):
    """
    Хэндлер для команды /voucher. Отправляет сообщение с просьбой ввести код ваучера
    и переводит пользователя в состояние ожидания кода ваучера.
    """
    await message.answer("🎫 Enter voucher code:")
    # Устанавливаем состояние ожидания ваучера
    await state.set_state(VoucherStates.waiting_for_voucher)
@router.message(StateFilter(VoucherStates.waiting_for_voucher))
async def process_voucher_input(message: Message, state: FSMContext):
    """
    Хэндлер для обработки ввода ваучера. Проверяет код ваучера через API
    и активирует подписку, если ваучер валиден.
    """
    # Извлекаем введённый код ваучера
    voucher_code = message.text.strip()

    # Отправляем запрос в API для проверки ваучера, передавая tgid и код ваучера
    response = await api.check_voucher(message.chat.id, voucher_code)

    # Проверяем ответ API
    if response["Success"]:
        await message.answer("The voucher has been activated! You have received a subscription.")
        # Логика активации подписки в API
        await api.process_voucher(message.chat.id, voucher_code)  # Активируем подписку через API
    else:
        await message.answer(f"Error: {response['Reason']}")

    # После обработки очищаем состояние
    await state.clear()
#--------------------------------------------------------------------------

@router.message(Command('help'))
async def help(message: types.Message):
    text, markup = await bot_logic.help_cmd(message.chat.id)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.message(Command('language'))
async def help(message: types.Message):
    text, markup = await bot_logic.language_cmd(message.chat.id)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на /admin
@router.message(Command('admin'))
async def admin(message: types.Message):
    r = await api.is_admin(message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admins_cmd(message)
        await message.answer(text, reply_markup=markup, )
#--------------------------------------------------------------------------
# #Хэндлер на любой текст 
@router.message(F.text)
async def anymsg(message: Message, bot: Bot, state: FSMContext):
    """
    Хэндлер для всех текстовых сообщений, который проверяет состояние пользователя.
    Если пользователь не вводит код ваучера, отображается стандартное меню.
    """
    # Проверяем текущее состояние пользователя
    current_state = await state.get_state()

    # Если пользователь не находится в состоянии ожидания ваучера
    if current_state != VoucherStates.waiting_for_voucher.state:
        text, markup = await bot_logic.menu_cmd(message)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

#|===========================[End Commands]===========================|




# CALLBACKS #
#|=============================[Utils]=============================|
# Обработчик для callback_data 'back'
@router.callback_query(F.data.startswith("menu "))
async def back(call: types.CallbackQuery):
    text, markup = await bot_logic.menu_cmd(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Коллбек на кнопку приятия соглашения 
@router.callback_query(F.data.startswith("agree "))
async def agree(call: types.CallbackQuery):
    text, markup = await bot_logic.agree(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("decline "))
async def decline(call: types.CallbackQuery):
    text, markup = await bot_logic.decline(call.message.chat.id)
    try:
        # Вместо редактирования сообщения, отправляем новое сообщение
        await call.bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    except Exception as e:
        print(f"Error sending message: {e}")
#|===========================[End utils]===========================|

#|=============================[Admin panel buttons]=============================|
# Обработчик для callback_data 'admin_users'
@router.callback_query(F.data.startswith("admin_users "))
async def admin_users(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_users(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_ban'
@router.callback_query(F.data.startswith("admin_ban "))
async def admin_ban(call: types.CallbackQuery):
    var = call.data.split(" ")
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_ban(call.message, var[2])
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_unban "))
async def admin_unban(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_unban(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher "))
async def admin_create_voucher(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_one "))
async def admin_create_voucher_one(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_one(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_six "))
async def admin_create_voucher_six(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_six(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_year "))
async def admin_create_voucher_year(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_year(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------


#|=============================[Menu buttons]=============================|
# Обработчик для callback_data 'config_gen'
@router.callback_query(F.data.startswith("config_gen "))
async def config_gen(call: types.CallbackQuery):
    text, markup = await bot_logic.config_gen(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'countries'
@router.callback_query(F.data.startswith("config_menu "))
async def config_menu(call: types.CallbackQuery):
    text, markup = await bot_logic.config_menu(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'delete'
@router.callback_query(F.data.startswith("delete "))
async def delete(call: types.CallbackQuery):
    await call.message.delete()
#--------------------------------------------------------------------------

# Обработчик для callback_data 'create_config'
@router.callback_query(F.data.startswith("create_config "))
async def create_config(call: types.CallbackQuery):
    """
    Обработчик для callback-запросов, связанных с выбором страны.
    
    Args:
        call (types.CallbackQuery): Объект callback-запроса.
    """
    try:
        _, tgid, hostname = call.data.split(" ")
        # Получаем текст, разметку и файл QR-кода от логики бота
        text, markup, markup_delete, qr_file = await bot_logic.create_config(call.message, hostname)

        if qr_file:
            # Попытка отправить файл как фото
            await call.message.answer_photo(
                photo=types.FSInputFile(qr_file), 
                caption=f"<code>{text}</code>", reply_markup=markup_delete
            )

            menu_text = f'''
                <b>Welcome to Spoof VeilVoyager 🌌</b>
_______________________

🚀 **Streamline your VPN setup effortlessly!**  
Experience seamless connectivity at your fingertips.

<b>Features:</b>
✨ <i>Create VPN configurations with a single click</i>

<b>Beta 0.7</b>
                '''
            
            await call.message.answer(text = menu_text, reply_markup=markup)

        else:
            # If no QR file, send only the text
            await call.message.answer(
                text=text,
                reply_markup=markup
            )
    except FileNotFoundError:
        # Handle case where file is not found
        await call.message.answer(
            text=f"File not found. Please try again later.\n<code>{text}</code>", 
            reply_markup=markup
        )
    except ValueError as ve:
        # Handle case where callback data is incorrect
        logging.error(f"Error in callback data: {ve}")
        await call.message.answer(
            text="Invalid data. Please try again.",
            reply_markup=markup
        )
    except Exception as e:
        # General error handling
        logging.error(f"Unknown error: {e}")
        await call.message.answer(
            text="An error occurred while processing your request.",
            reply_markup=markup
        )
#--------------------------------------------------------------------------

# Обработчик для callback_data 'learn more'
@router.callback_query(F.data.startswith("learn_more "))
async def learn_more(call: types.CallbackQuery):
    text, markup = await bot_logic.learn_more(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'learn more'
@router.callback_query(F.data.startswith("en_language "))
async def en_language(call: types.CallbackQuery):
    lang = "en"
    text, markup = await bot_logic.set_language(call.message, lang)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'learn more'
@router.callback_query(F.data.startswith("ru_language "))
async def ru_language(call: types.CallbackQuery):
    lang = "ru"
    
    # Логируем перед вызовом функции
    logging.info(f"User {call.from_user.id} selected language: {lang}")
    
    # Пробуем вызвать функцию и логируем результат
    try:
        text, markup = await bot_logic.set_language(call.message, lang)
        logging.info("Language set successfully, preparing to edit message.")
    except Exception as e:
        logging.error(f"Error while setting language: {e}")
        await call.message.answer("Произошла ошибка при смене языка.")
        return
    
    # Редактируем текст сообщения после успешного изменения
    await call.message.edit_text(text=text, reply_markup=markup)

#--------------------------------------------------------------------------
# Обработчик для callback_data 'account_menu'
@router.callback_query(F.data.startswith("account_menu "))
async def account_menu(call: types.CallbackQuery):
    text, markup = await bot_logic.account_menu(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("top_up_balance "))
async def top_up_balance(call: types.CallbackQuery):
    text, markup = await bot_logic.top_up_balance(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("pay_subscription "))
async def pay_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("account_settings "))
async def account_settings(call: types.CallbackQuery):
    text, markup = await bot_logic.account_settings(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("pay_with_crypto "))
async def pay_with_crypto(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_crypto(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("one_month_subscription "))
async def one_month_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.one_month_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("six_months_subscription "))
async def six_months_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.six_months_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("year_subscription "))
async def year_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.year_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
