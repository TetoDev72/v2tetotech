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
