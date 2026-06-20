Project Path: docs

Source Tree:

```txt
docs
├── DEBUG_ENDPOINTS.md
├── MISC_ENDPOINTS.md
├── PAYLOAD_DATA.md
├── SYNC.md
└── USECASES.md

```

`DEBUG_ENDPOINTS.md`:

```md
# Диагностические и debug эндпоинты
## Headers (заголовки клиента)
Добавьте эту ссылку в закрытый клиент, чтобы посмотреть, какие заголовки он отдает. Возвращает как vless ключи, так что в клиенте будут видны данные запроса

### Как использовать
{v2tetotech url}/headers
{v2tetotech url}/h

## Default spoofing data
Возвращает дефолтные данные, под которые максируется сервер.

### Как использовать
{v2tetotech url}/spoofdata?strategy=best
{v2tetotech url}/sd?strategy=best

## Server info
Возвращает версию API, список зеркал и статус текущего сервера. Создан как заглушка для базового пинга.

### Как использовать
{v2tetotech url}/svinfo
{v2tetotech url}/v

```

`MISC_ENDPOINTS.md`:

```md
# Другие эндпоинты
## Decrypt
Декриптит криптоссылки. Отдает дешифрованную ссылку, обернутую в JSON.

### Как использовать
{v2tetotech url}/decrypt?link=happ://crypt5/xyz123...
{v2tetotech url}/e?link=happ://crypt5/xyz123...

## Deeplink maker
Создает диплинки для запрошенного клиента и отдает их в JSON.

### Как использовать
{v2tetotech url}/deeplink?url=https://example.com&client=mihomo&mode=sync&base_url={v2tetotech url}
{v2tetotech url}/d?url=https://example.com&client=mihomo&mode=sync&base_url={v2tetotech url}

## Генератор пейлоадов
Автоматически создает payload data под ссылку и отдает ссылку, которая уже знает как обходить блокировки.

### Как использовать
{v2tetotech url}/payloadgen?link=https://example.com&strategy=best&base_url={v2tetotech url}
{v2tetotech url}/y?link=https://example.com&strategy=best&base_url={v2tetotech url}
{v2tetotech url}/pg?link=https://example.com&strategy=best&base_url={v2tetotech url}

## Клей подписок
Собирает несколько подписок в одну большую подписку под одной ссылкой.

### Как использовать
{v2tetotech url}/batch?urls=https://sub1.com,https://sub2.com,happ://crypt5/xyz...
{v2tetotech url}/b?urls=https://sub1.com,https://sub2.com,happ://crypt5/xyz...

```

`PAYLOAD_DATA.md`:

```md
# Payload data
Payload data - формат пейлоада для v2tetotech /advsync или /x эндпоинта

## Примеры
- Дефолтные параметры - "link=https://example.com/sub,format=auto"
- Happ Crypt + branding - "link=happ://crypt5/abc...,hwid=default,ua=happ,title=Халява,webpage=https://example.com,format=auto"

## Параметры
### Основные
- link - ссылка на подписку или криптоссылка (обязательный параметр, не принимает особые значения)
- format - формат, в котором отдать подписку (принимает auto, clash, sing-box, xray, v2ray)
- chain - скорее для fallback и стабильности, цепь по которому v2tetotech перебирает заголовки (пример happ,v2plus,chrome)

### Заголовки и спуфинг
- hwid - hardware id, или проще говоря ID устройства (принимает default (CRC16 хеш ссылки), или кастомный HEX длиной 16 символов)
- ua/client - User Agent клиента (принимает happ, v2rayng, clash, singbox, nekobox, v2plus, v2rayn, mihomo, singbox, sfa, hiddify, shadowrocket, stash, streisand, foxray)
- os - операционная система клиента (принимает android, ios, windows, macos, linux)
- model - модель устройства (принимает строку, к примеру ELP-NX1, SN-S928B, Pixel 10 Pro XL)
- osver - версия ОС (к примеру 13, 14, 15)
- realip - X-Real-Ip заголовок (к примеру 91.232.180.41, также принимает random и default) 
- forwardedfor - X-Forwared-For заголовок (к примеру 91.232.180.41, также принимает random и default)

### Брендинг (мета подписки)
- title - название подписки (к примеру "Халявная подписка")
- webpage - веб страница поддержки (к примеру https://example.com)
- updateint - интервал автообновления подписки в часах (к примеру 24)
- lastupd - дата последнего обновления (к примеру 2008-04-01)
- announce - описание (к примеру "Сервера могут использоваться при белых списках!")

```

`SYNC.md`:

```md
# Список эндпоинтов получения подписок
## /auto или /i
### Для чего?
Предназначен для обычных пользователей, которые хотят подключить VPN. Автоматически генерирует HWID, маскируется под Happ. Не принимает параметров, но зато имеет максимально простой синтаксис и берет всю работу на себя, но выдает сырые данные, а значит не поддерживает SFA/Mihomo

### Использование
{v2tetotech url}/auto/(url подписки или же happ://crypt* просто так или в base64)
{v2tetotech url}/i/(url подписки или же happ://crypt* просто так или в base64)

## /fetch или /f
### Для чего?
Предназначен для обычных или продвинутых пользователей, которые хотят добавить подписку НЕ ЗАЛОЧЕННУЮ ПОД HWID в несовместимый клиент (raw xray-core, sing-box for android, mihomo), требующие свой формат. Не отправляет HWID и не имеет параметров

### Использование
{v2tetotech url}/fetch/(url подписки или же happ://crypt* просто так или в base64)
{v2tetotech url}/f/(url подписки или же happ://crypt* просто так или в base64)

## /sync или /s
### Для чего?
Предназначен для обычных пользователей, которые хотят подключить VPN, но уже в Mihomo/SFA. Автоматически генерирует HWID, маскируется под Happ. Не принимает параметров, но зато имеет максимально простой синтаксис и берет всю работу на себя, формат определяет по User-Agent клиента.

### Использование
{v2tetotech url}/sync/(url подписки или же happ://crypt* просто так или в base64)
{v2tetotech url}/s/(url подписки или же happ://crypt* просто так или в base64)

## /advsync или /x
Самый продвинутый роут, предназначен для контроля данными и создания ссылок с особым брендингом. Обычным пользователям не требуется. Также поддерживает фильтры и автопинг (удаление конфигов-заглушек, к примеру с 0.0.0.0 или фильтрация метрвых конфигов). Для конфигурации нужно составить Payload Data, об этом подробнее в PAYLOAD_DATA.md. Также может быть создано генератором payload-ов

### Использование
{v2tetotech url}/advsync?p=(payload data encoded in base64)
{v2tetotech url}/x?p=(payload data encoded in base64)

```

`USECASES.md`:

```md
# Кейсы использования

## Спуфинг и байпасс
- Автоматически обходить блокировки по User-Agent (Happ передает привет)
- Дешифровать конфиги happ://crypt* прозрачно
- Делать HWID на основе ссылки по CRC-16
- Быть всегда предсказуемым, что делает всего одно устройство в боте 
- Работать как одна ссылка, обновляемая через сам клиент

## Автоматизация
- Публичный API для всех возможностей сервера
- Fetch режим для конвертации не HWID подписок под Clash формат
- Advsync режим для получения Happ подписок и удаления заглушек и нерабочих (идеально для парсеров)
- Decrypt эндпоинт спецально для парсеров
- Брендинг для замены названий и описаний подписок

## Обычные пользователи
- Использование Mihomo клиентов когда провайдер их не поддерживает
- Обход блокировки Happ, если провайдер требует его
- Обход happ://crypt*
- Безопасный, полностью автоматизированный обход устройств
- Максимально внутренний опыт, а значит клиент будет вести себя абсолютно также, как при обычной ссылке

```