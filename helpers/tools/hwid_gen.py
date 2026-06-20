def generate_hwid_from_url(url: str) -> str:
    if not url:
        return "0000000000000000"
        
    crc = 0xFFFF
    for byte in url.encode('utf-8'):
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
                
    return f"{crc:016X}"
