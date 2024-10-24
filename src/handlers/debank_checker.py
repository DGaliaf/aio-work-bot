import io

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, BufferedInputFile

from src.keyboards import debank_inline_keyboard, debank_leave_inline_keyboard
from src.services.checkers.debank.debank import Debank
from src.states import DeBank
from src.utils import is_wallet, get_wallets

router: Router = Router()


@router.callback_query(lambda c: c.data == 'debank_checker')
async def debank_checker(callback: types.CallbackQuery):
    checkers_msg = "Добро пожаловать в <b>DeBank чекер</b>\n\nВыберите режим работы:"

    await callback.message.edit_text(text=checkers_msg, reply_markup=debank_inline_keyboard)


@router.callback_query(lambda c: c.data == 'debank_single_parse')
async def debank_single_parse(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DeBank.wallet)

    msg = ("<b>Одиночный режим DeBank</b>\n\nОтправь кошелек и получи баланс!\nЧтобы выйти из этого режима "
           "нажмите - <b>'Выйти</b>'")

    debank = Debank()

    callback_message = await callback.message.answer(text="Отправьте адрес кошелька")
    await state.set_data({"msg_id": callback_message.message_id, "debank": debank})

    await callback.message.edit_text(text=msg, reply_markup=debank_leave_inline_keyboard)


@router.message(DeBank.wallet, F.text)
async def check_single_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()

    debank: Debank = data.get("debank")

    await message.delete()

    if not is_wallet(message.text):
        await message.bot.edit_message_text(text=f"Проверьте правильность адреса - {message.text}",
                                            chat_id=message.chat.id, message_id=data.get("msg_id"))
    else:
        response = await debank.api("GET", "/user", {"query": {"id": message.text.strip()}})

        user_data = response.get("user")
        balance = user_data.get("stats").get("usd_value")

        if balance is None:
            balance = user_data.get("desc").get("usd_value")

        balance = round(balance)

        await message.bot.edit_message_text(text=f"Баланс адреса {message.text} - ${balance}", chat_id=message.chat.id,
                                            message_id=data.get("msg_id"))


@router.callback_query(lambda c: c.data == 'debank_multiple_parse')
async def debank_multiple_parse(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DeBank.wallets)

    msg = ("<b>Файловый режим DeBank</b>\n\nОтправь кошельки и получи баланс!\nЧтобы выйти из этого режима "
           "нажмите - <b>'Выйти</b>'")

    debank = Debank()

    callback_message = await callback.message.answer(text="<b>Отправьте файл с адресами кошельков</b>\nИли же\n<b>Отправьте адреса кошельков (каждый адрес с новой строки)</b>", parse_mode="HTML")
    await state.set_data({"msg_id": callback_message.message_id, "debank": debank})

    await callback.message.edit_text(text=msg, reply_markup=debank_leave_inline_keyboard)


@router.message(DeBank.wallets)
async def check_multiple_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()

    wallets = []
    if message.text is not None and message.document is None:
        wallets = get_wallets(message.text.split("\n"))

    if message.text is None and message.document is not None:
        file = await message.bot.get_file(message.document.file_id)
        result: io.BytesIO = await message.bot.download_file(file.file_path)

        wallets = [line.strip().decode("utf-8") for line in result.readlines()]

    if message.text is None and message.document is None:
        await message.bot.edit_message_text(text=f"Отправьте либо файл с адресами, либо текст с адресами",
                                            chat_id=message.chat.id, message_id=data.get("msg_id"))

    debank: Debank = data.get("debank")

    await message.delete()

    tot = len(wallets)
    cur = 1

    output = io.BytesIO()

    for wallet in wallets:
        print(f"{cur}/{tot}")
        await message.bot.edit_message_text(text=f"Проверяю кошельки - {cur}/{tot}",
                                            chat_id=message.chat.id, message_id=data.get("msg_id"))

        response = await debank.api("GET", "/user", {"query": {"id": wallet.strip()}})
        user_data = response.get("user")

        balance = user_data.get("stats").get("usd_value")
        if balance is None:
            balance = user_data.get("desc").get("usd_value")
        balance = round(balance)

        output.write(f'{wallet}:{balance}\n'.encode('utf-8'))

        await state.update_data(balances=output.read())

        cur += 1

    output.seek(0)

    file = BufferedInputFile(output.read(), filename=f"output.txt")

    output.close()

    await message.bot.send_document(chat_id=message.chat.id, document=file)

