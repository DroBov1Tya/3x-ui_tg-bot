import qrcode
import random
import logging
import os
import base64
from string import ascii_letters, digits

logger = logging.getLogger(__name__)
ascii_letdigest = ascii_letters + digits

#|=============================[Config Generator]=============================|
async def create_config(inbound_data: dict) -> str:
    """
    Создаёт конфигурацию и QR-код для клиента на основе данных inbound.

    Args:
        inbound_data (dict): Словарь с данными inbound для генерации конфигурации.

    Returns:
        str: Сгенерированная конфигурационная строка URL.
    """
    try:
        config_variables = {
        "id" : inbound_data["client_id"],
        "ip" : inbound_data["hostname"],
        "port" : inbound_data["port"],
        "type" : inbound_data["network"],
        "security" : inbound_data["security"],
        "pbk" : inbound_data["public_key"],
        "fp" : inbound_data["fingerprint"],
        "sni" : "yahoo.com",
        "sid" : inbound_data["short_ids"][(random.randint(0, 7))],
        "remark" : inbound_data["remark"],
        "client" : inbound_data["email"]
        }

        config = f'''vless://\
        {config_variables["id"]}@\
        {config_variables["ip"]}:\
        {config_variables["port"]}/?\
        type={config_variables["type"]}&\
        security={config_variables["security"]}&\
        pbk={config_variables["pbk"]}&\
        fp={config_variables["fp"]}&\
        sni={config_variables["sni"]}&\
        sid={config_variables["sid"]}#\
        {config_variables["remark"]}-\
        {config_variables["client"]}'''

        # Убираем лишние пробелы и переносы строк
        url = config.replace("\n", "").replace(" ", "")

        qr = qrcode.QRCode(box_size=10,)
        qr_filename = config_variables["client"]
        qr.add_data(url)
        img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
        img.save(f"./qr_code/{qr_filename}.png")

        with open(f"./qr_code/{qr_filename}.png", "rb") as f:
            qr_data = base64.b64encode(f.read()).decode("utf-8")

        return url, qr_data

    except KeyError as e:
        logger.error("Отсутствует ключ в inbound_data: %s", e)
        return ""
    except Exception as ex:
        logger.error("Ошибка при создании конфигурации: %s", ex)
        return ""
#--------------------------------------------------------------------------

#|=============================[Generate Random SID]=============================|
async def random_short_ids() -> list:
    """
    Генерирует список случайных shortIds на основе перемешанных длин.

    Returns:
        list: Список сгенерированных коротких идентификаторов (shortIds).
    """
    # Список возможных длин shortId
    lengths = [2, 4, 6, 8, 10, 12, 14, 16]

    # Перемешиваем список длин
    random.shuffle(lengths)

    # Последовательность символов для генерации shortId
    seq = '0123456789abcdef'

    # Генерация shortIds
    short_ids = [''.join(random.choice(seq) for _ in range(length)) for length in lengths]

    return short_ids
#--------------------------------------------------------------------------

#|=============================[String Generator]=============================|
async def string_generator(type: str, length: int) -> str:
    """
    Генерирует случайную строку на основе типа и длины.

    Args:
        type (str): Тип строки ("letter" - только буквы, "letdiggest" - буквы и цифры).
        length (int): Длина генерируемой строки.

    Returns:
        str: Сгенерированная строка или None, если тип не распознан.
    """
    if length <= 0:
        return None  # Защита от неправильной длины

    if type == "letter":
        # Генерация строки только из букв
        return ''.join(random.choices(ascii_letters, k=length))
    
    elif type == "letdiggest":
        # Генерация цифро-буквенной строки
        return ''.join(random.choices(ascii_letdigest, k=length))
    
    else:
        return None  # Если передан неправильный тип
#--------------------------------------------------------------------------