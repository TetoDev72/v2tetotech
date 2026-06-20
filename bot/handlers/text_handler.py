from aiogram import Router, F
from aiogram.types import Message
import urllib.parse
from v2ttclient import v2tt

router = Router()

def is_link(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://") or text.startswith("happ://")

@router.message(F.text)
async def handle_text(message: Message, selected_server: str):
    text = message.text.strip()
    if not is_link(text):
        return

    link = text
    await message.answer("⏳ Обрабатываю ссылку...")
    results = []

    if link.startswith("happ://crypt"):
        try:
            dec_result = await v2tt.call("DECRYPT", {"link": link}, selected_server)
            results.append(f"🔓 **Дешифрованная:**\n`{dec_result['url']}`")
            link = dec_result['url']
        except Exception as e:
            results.append(f"❌ Decrypt error: {e}")

    auto_url = f"{selected_server}/auto/{urllib.parse.quote(link, safe='')}"
    results.append(f"⚡ **Auto:**\n`{auto_url}`")

    try:
        sync_result = await v2tt.call("DEEPLINK", {
            "url": link,
            "mode": "sync",
            "client": "v2rayng",
            "base_url": selected_server
        }, selected_server)
        results.append(f"🔗 **Sync:**\n`{sync_result['subscription_url']}`")
    except Exception as e:
        results.append(f"❌ Sync error: {e}")

    try:
        wl_result = await v2tt.call("WHITELIST_BYPASS_LINK", {
            "url": link,
            "strategy": "yandex_translate"
        }, selected_server)
        results.append(f"🛡️ **WL Bypass:**\n`{wl_result['url']}`")
    except Exception:
        pass

    final_text = "\n".join(results)
    await message.answer(final_text, parse_mode="Markdown")
