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
