from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import base64
import urllib.parse
from v2ttclient import v2tt

router = Router()

class PayloadConstructor(StatesGroup):
    waiting_for_link = State()
    waiting_for_params = State()
    waiting_for_edit = State()

@router.message(Command("sync"))
async def cmd_sync(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /sync (ссылка)")
        return
    link = args[1].strip()
    try:
        result = await v2tt.call("DEEPLINK", {
            "url": link, "mode": "sync", "client": "v2rayng", "base_url": selected_server
        }, selected_server)
        text = f"✅ **Sync ссылка готова!**\n"
        text += f"🔗 `{result['subscription_url']}`\n"
        text += f"📱 **Диплинки:**\n"
        for client_name, dl in result['all_deeplinks'].items():
            text += f"• **{client_name}**: `{dl}`\n"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("fetch"))
async def cmd_fetch(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /fetch (ссылка)")
    link = args[1].strip()
    try:
        result = await v2tt.call("DEEPLINK", {
            "url": link, "mode": "fetch", "client": "v2rayng", "base_url": selected_server
        }, selected_server)
        text = f"✅ **Fetch ссылка готова!**\n🔗 `{result['subscription_url']}`\n"
        text += f"📱 **Диплинки:**\n"
        for client_name, dl in result['all_deeplinks'].items():
            text += f"• **{client_name}**: `{dl}`\n"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("auto"))
async def cmd_auto(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /auto (ссылка)")
    link = args[1].strip()
    auto_url = f"{selected_server}/auto/{urllib.parse.quote(link, safe='')}"
    await message.answer(f"✅ **Auto ссылка готова!**\n🔗 `{auto_url}`", parse_mode="Markdown")

@router.message(Command("decrypt"))
async def cmd_decrypt(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /decrypt (ссылка)")
    link = args[1].strip()
    try:
        result = await v2tt.call("DECRYPT", {"link": link}, selected_server)
        await message.answer(f"🔓 **Дешифрованная ссылка:**\n`{result['url']}`", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка дешифровки: {e}")

@router.message(Command("charity"))
async def cmd_charity(message: Message, selected_server: str):
    try:
        result = await v2tt.call("CHARITY", {}, selected_server)
        text = f"🎁 **Charity подписка:**\n`{result['subscription'][:100]}...`\n"
        text += f"💝 Спасибо разработчикам за бесплатную подписку!"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("pg"))
async def cmd_pg(message: Message, command: Command, state: FSMContext, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.answer("❌ Использование: /pg (ссылка)\nИли отправь ссылку и нажми кнопку 'Конструктор'")
    link = args[1].strip()
    await state.update_data(link=link)
    await state.set_state(PayloadConstructor.waiting_for_params)
    text = f"🔧 **Интерактивный конструктор payload**\n🔗 Ссылка: `{link}`\n"
    text += f"Введите параметры в формате:\n`hwid=default,ua=happ,title=My Sub,format=auto`\n"
    text += f"Или отправьте `default` для использования настроек по умолчанию."
    await message.answer(text, parse_mode="Markdown")

@router.message(PayloadConstructor.waiting_for_params)
async def process_params(message: Message, state: FSMContext, selected_server: str):
    data = await state.get_data()
    link = data.get("link")
    if not link:
        await message.answer("❌ Ошибка: ссылка не найдена")
        return await state.clear()

    try:
        result = await v2tt.call("PAYLOAD_GEN", {
            "link": link, "strategy": "best", "base_url": selected_server
        }, selected_server)

        text = f"✅ **Payload ссылка готова!**\n🔗 `{result['v2tetotech_link']}`\n"
        text += f"📱 **Диплинки:**\n"
        for client_name, dl in result['deeplinks'].items():
            text += f"• **{client_name}**: `{dl}`\n"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    finally:
        await state.clear()

@router.message(Command("wlify"))
async def cmd_wlify(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /wlify (ссылка)")
    link = args[1].strip()
    try:
        result = await v2tt.call("WHITELIST_BYPASS_LINK", {
            "url": link, "strategy": "yandex_translate"
        }, selected_server)
        text = f"🛡️ **Whitelist bypass ссылка готова!**\n🔗 `{result['url']}`\n"
        text += f"💡 Эта ссылка обходит российские whitelist блокировки!"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("deeplink"))
async def cmd_deeplink(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /deeplink (ссылка)")
    link = args[1].strip()
    try:
        result = await v2tt.call("DEEPLINK", {
            "url": link, "mode": "sync", "client": "v2rayng", "base_url": selected_server
        }, selected_server)
        text = f"🔗 **Диплинки готовы!**\n📱 **Subscription URL:**\n`{result['subscription_url']}`\n"
        text += f"📱 **Диплинки:**\n"
        for client_name, dl in result['all_deeplinks'].items():
            text += f"• **{client_name}**: `{dl}`\n"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("batch"))
async def cmd_batch(message: Message, command: Command, selected_server: str):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /batch (ссылки через пробел)")
    links = [l.strip() for l in args[1].strip().split() if l.strip()]
    if not links: return await message.answer("❌ Не найдено ссылок")
    try:
        result = await v2tt.call("BATCH", {"urls": ",".join(links)}, selected_server)
        text = f"📦 **Batch ссылка готова!**\nСклеено ссылок: **{result['count']}**\n`{result['subscription'][:100]}...`"
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@router.message(Command("editor"))
async def cmd_editor(message: Message, command: Command, state: FSMContext):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.answer("❌ Использование: /editor (sync или advsync ссылка)")
    link = args[1].strip()
    await state.update_data(edit_link=link)
    await state.set_state(PayloadConstructor.waiting_for_edit)
    text = f"✏️ **Интерактивный редактор**\n🔗 Ссылка: `{link}`\nВведите новые параметры:\n`title=New Title,webpage=https://new.com`\nИли отправьте `skip`."
    await message.answer(text, parse_mode="Markdown")

@router.message(PayloadConstructor.waiting_for_edit)
async def process_edit(message: Message, state: FSMContext, selected_server: str):
    params_text = message.text.strip()
    data = await state.get_data()
    link = data.get("edit_link")
    if not link:
        await message.answer("❌ Ошибка: ссылка не найдена")
        return await state.clear()
    if params_text.lower() == "skip":
        await message.answer("⏭️ Редактирование пропущено")
        return await state.clear()

    try:
        params = {}
        for pair in params_text.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k.strip()] = v.strip()
        params["link"] = link

        result = await v2tt.call("ADVANCED_SYNC", params, selected_server)
        await message.answer(f"✅ **Ссылка обновлена!**\n`{result['content'][:100]}...`", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
    finally:
        await state.clear()
