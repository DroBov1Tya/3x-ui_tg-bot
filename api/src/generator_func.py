import pyqrcode
import random
from string import ascii_letters, digits

ascii_letdigest = ascii_letters + digits

#|=============================[Config Generator]=============================|
async def create_config(inbound_data):
    config_variables = {
    "id" : inbound_data["client_id"],
    "ip" : "191.96.235.118",
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
    url = config.replace("\n", "").replace(" ", "")
    qr = pyqrcode.create(url)
    qr.png(f'qr_code/{config_variables["client"]}.png')
#--------------------------------------------------------------------------

#|=============================[Generate Random SID]=============================|
async def random_short_ids():
        lengths = [2, 4, 6, 8, 10, 12, 14, 16]
        
        # Перемешиваем список lengths
        for i in range(len(lengths) - 1, 0, -1):
            j = random.randint(0, i)
            lengths[i], lengths[j] = lengths[j], lengths[i]

        # Генерация случайных shortId
        short_ids = []
        seq = '0123456789abcdef'  # последовательность из 16 символов

        for length in lengths:
            short_id = ''.join(random.choice(seq) for _ in range(length))
            short_ids.append(short_id)

        return short_ids
#--------------------------------------------------------------------------

#|=============================[String Generator]=============================|
async def string_generator(type: str, lenght):
    '''
    gavnogavnogavnogavnogavnogavno
    '''

    return_variable = str()
    if type == "letter":
        for i in range(1, lenght):
            return_variable += ascii_letters[random.randint(1, 50)]
    elif type == "letdiggest":
        for i in range(1, lenght):
            return_variable += ascii_letdigest[random.randint(1, 60)]
    else:
        return None
    return str(return_variable)
#--------------------------------------------------------------------------