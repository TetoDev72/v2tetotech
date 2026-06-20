# v2tetotech API
v2tetotech предоставляет разработчикам полностью бесплатный публичный API!

## Условия использования
API можно использовать абсолютно бесплатно и свободно, но было бы хорошо, если вы укажете, что API наш. Хотя мы абсолютно не против, если вы используете наш API, можете даже поднять свой сервер v2tetotech и поддержать проект ;)

## Базовый формат
API имеет единый endpoint **/api**, или /a, действие обозначается командой в POST-запросе.

Запрос (POST):
```json
{
  "cmd": "COMMAND_NAME",
  "role": "REQUEST",
  "data": { ... }
}
```
Ответ:
```json
{
  "cmd": "COMMAND_NAME",
  "role": "RESPONSE",
  "data": { ... }
}
```

Далее названия разделов будут командными кодами, а предоставлен будет контент data, его обернуть в базовый запрос.
К примеру финальный ответ PING:
```json
{
  "cmd": "PING",
  "role": "RESPONSE",
  "data": {
    "pong": "hello!",
    "timestamp": "2026-06-20T12:00:00.000000",
    "version": "2.0.0"
  }
}
```
Все коды (для удобства): PING, SERVER_INFO, HWID, DECRYPT, HEADERS, DEVICE, DEEPLINK, CHARITY, BATCH, SYNC, FETCH, ADVANCED_SYNC, PAYLOAD_GEN

## PING
Проверка доступности сервера и вывод его версии.
Запрос:
```json
{
  "cmd": "PING",
  "data": {}
}
```

Ответ:
```json
{
  "pong": "hello!",
  "timestamp": "2026-06-20T12:00:00.000000",
  "version": "2.0.0"
}
```
## HWID
Генерирует HWID для ссылки (липкий, предсказуемый CRC16)
Запрос:
```json
{
  "cmd": "HWID",
  "data": {
    "url": "https://example.com/sub"
  }
}
```

Ответ:
```json
{
  "hwid": "A1B2C3D4E5F60718",
  "url": "https://example.com/sub",
  "algorithm": "CRC-16/ARC"
}
```

## DECRYPT
Дешифрует криптоссылки.
Запрос:
```json
{
  "cmd": "DECRYPT",
  "data": {
    "link": "happ://crypt5/xyz123..."
  }
}
```

Ответ:
```json
{
  "status": "success",
  "url": "https://real-sub.com/..."
}
```

## HEADERS
Возвращает заголовки клиента как vless:// ключи.
Запрос:
```json
{
  "cmd": "HEADERS",
  "data": {}
}
```

## DEVICE
Возвращает заголовки клиента как vless:// ключи.
Запрос:
```json
{
  "cmd": "DEVICE",
  "data": {}
}
```

## DEEPLINK
Делает ссылку v2tetotech с вашим base url и из нее уже deeplink запрошенного клиента.
Запрос:
```json
{
  "cmd": "DEEPLINK",
  "data": {
    "url": "https://example.com/sub",
    "client": "mihomo",
    "mode": "sync",
    "base_url": "https://your-v2tetotech-url.com"
  }
}
```

Ответ:
```json
{
  "client": "mihomo",
  "mode": "sync",
  "subscription_url": "https://your-v2tetotech-url.com/s/...",
  "deeplink": "clash://install-config?url=https://your-v2tetotech-url.com/s/...",
  "all_deeplinks": { "clash": "...", "v2rayng": "...", "singbox": "..." }
}
```

## CHARITY
Возвращает подписку на благотворительность от v2tetotech.
Запрос:
```json
{
  "cmd": "CHARITY",
  "data": {}
}
```

## BATCH
Возвращает большую подписку, склееную из списка в запросе, включая happ://crypt*.
Запрос:
```json
{
  "cmd": "BATCH",
  "data": {
    "urls": "https://sub1.com,https://sub2.com,happ://crypt5/xyz..."
  }
}
```

## SYNC
Получение подписки, с авто HWID и UA.
Запрос:
```json
{
  "cmd": "SYNC",
  "data": {
    "url": "https://example.com/sub",
    "hwid": "default",
    "client": "happ"
  }
}
```

## FETCH
Получение подписки, без спуфинга.
Запрос:
```json
{
  "cmd": "SYNC",
  "data": {
    "url": "https://example.com/sub",
    "client": "mihomo"
  }
}
```

## ADVANCED_SYNC
Продвинутый SYNC с полным контролем над спуфингом, HWID и брендингом. Принимает те же параметры, что и payload data в /advsync.
Запрос:
```json
{
  "cmd": "ADVANCED_SYNC",
  "data": {
    "link": "https://example.com/sub",
    "hwid": "default",
    "ua": "happ",
    "title": "Халява",
    "format": "auto"
  }
}
```

## PAYLOAD_GEN
Делает готовую ссылку для /advsync с зашитым payload data (авто-создание) и набором диплинков. Для выдачи ссылки автоматически, к примеру в Telegram-ботах.
Запрос:
```json
{
  "cmd": "PAYLOAD_GEN",
  "data": {
    "link": "https://example.com/sub",
    "strategy": "best",
    "base_url": "https://your-v2tetotech-url.com"
  }
}
```
Ответ:
```json
{
  "cmd": "PAYLOAD_GEN",
  "role": "RESPONSE",
  "data": {
    "strategy_used": "best",
    "selected_profile": {
      "hwid": "F4E2A1B9C8D7E6F5",
      "ua": "Happ/3.13.0 (Android 15; ELP-NX1)",
      "os": "Android",
      "model": "ELP-NX1",
      "osver": "15",
      "realip": "random",
      "forwardedfor": "random",
      "link": "https://example.com/sub"
    },
    "payload_string": "hwid=F4E2A1B9C8D7E6F5,ua=Happ/3.13.0 (Android 15; ELP-NX1),os=Android,model=ELP-NX1,osver=15,realip=random,forwardedfor=random,link=https://example.com/sub",
    "payload_base64": "aHdpZD1GNEUyQTFCOUM4RDdFNkY1LHVhPUhhcHAvMy4xMy4wIChBbmRyb2lkIDE1OyBFTFAtTlgxKSxvcz1BbmRyb2lkLG1vZGVsPUVMUC1OWDEsb3N2ZXI9MTUscmVhbGlwPXJhbmRvbSxmb3J3YXJkZWRmb3I9cmFuZG9tLGxpbms9aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWI=",
    "v2tetotech_link": "https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUyQTFCOUM4RDdFNkY1LHVhPUhhcHAvMy4xMy4wIChBbmRyb2lkIDE1OyBFTFAtTlgxKSxvcz1BbmRyb2lkLG1vZGVsPUVMUC1OWDEsb3N2ZXI9MTUscmVhbGlwPXJhbmRvbSxmb3J3YXJkZWRmb3I9cmFuZG9tLGxpbms9aHR0cHM6Ly9leGFtcGxlLmNvbS9zdWI=",
    "deeplinks": {
      "v2rayng": "v2rayng://install-sub?url=https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy...",
      "clash": "clash://install-config?url=https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy...",
      "singbox": "sing-box://import-remote-profile?url=https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy...#v2tetotech",
      "nekobox": "nekobox://import-remote-profile?url=https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy...",
      "happ": "happ://import/https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy...",
      "v2plus": "v2plus://import/https://node1.v2teto.tech/advsync?p=aHdpZD1GNEUy..."
    },
    "mode": "sync"
  }
}
```
