import googletrans
import requests
import asyncio
from dotenv import dotenv_values
from twilio.rest import Client
from googletrans import Translator

def test_installation(phonenum_to, phonenum_from, body):
    # Your Account SID and Auth Token from console.twilio.com
    config = dotenv_values(".env")
    account_sid = config['API-Key-SID']
    auth_token = config['API-Key-secret']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=phonenum_to,
        from_=phonenum_from,
        body=body)
    return message.sid




async def translate_message(text, source=None, dest=None):
    """Fetches the translation of 'text'
    :param
    :return: translated text
    """
    async with Translator() as translator:
        result = await translator.translate(text)
    return result



def main():
    test = asyncio.run(translate_message("No hay mal que por bien no venga", 'es', 'la'))
    print(test)



if __name__ == '__main__':
    main()

#phonenum1 = "+493083795321", phonenum2 = "+491775252784"
