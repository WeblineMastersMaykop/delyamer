from requests_oauthlib import OAuth2Session


oauth = OAuth2Session(
    client_id='891a81a8-0e2e-4988-81d6-429a40d98625',
    # client='fdwZM6jQsxz66b3aTVpPRmyzY7iZZJxLQoBxwmvPz4eB7pmKQ2xAOXRr5AcaMtex',
    auto_refresh_url='https://goga23d.amocrm.ru/oauth2/access_token',
    auto_refresh_kwargs={
        'client_id': '891a81a8-0e2e-4988-81d6-429a40d98625',
        'client_secret': 'fdwZM6jQsxz66b3aTVpPRmyzY7iZZJxLQoBxwmvPz4eB7pmKQ2xAOXRr5AcaMtex',
    },
    # scope=None,
    redirect_uri='http://localhost.ru',
    # token=None,
    # state=None,
    # token_updater=None,
)

token = oauth.fetch_token(
        'https://goga23d.amocrm.ru/oauth2/access_token',
        code='def502008aa20698b48cad0a1b9f799940da625993ef96344ca0f2fc7d090c3b1b53026550a9ef88a629c5f2b1ab40850f0be096da27b17d5c513e071700eced011c8572871522138f96a5046ddd2e610b8010b5a3e5c8cca30e738dbb8f16c87aeb6e5642f1bc4a77f536ffe7601ac6ad2a4b94395b366716c421a329a6789733a075614f45764cc61731378f41161cea6d1bb008f7d3252fd959f7d5c7e9846b8a2f1e668ff814e8ca1d0d4de9746dc74412bd5b5289cdf2f95823f5e976a81a4a2fba8c7b9ee0b1ecacafd36fcbfccdfb5fadb5b71d79f2dc4692c3dc6cca1e7dba27d14d63b3be6ec2bb06736020aebf38adb52e35e587ae67d52d6827b39817b6ab68fccbdaa15662d98b051d96f04d2daddb27b91700ca239b8d2bcc13f6aec1608befd8498f94623081600cb20b82ef5ed5762ddf4dfc72a698b5d1cb949e0fdfe946eb410ca644b6b60bc8da7620c21696dd85cf7f7dc437e99d6539da9fe0a624ba0b5271b4999f9891bfb00354fc04ddcf602f3f44c3cd0a8e5af7173e2aa46b72da577e013a7fb08e3245191b1d48ccfc1b983c7bdb3c74539da2d1e286d79fae3faf42c339cb5c91a9c056e0bc1013bef40a87b86f7247',
        client_id='891a81a8-0e2e-4988-81d6-429a40d98625',
        client_secret='fdwZM6jQsxz66b3aTVpPRmyzY7iZZJxLQoBxwmvPz4eB7pmKQ2xAOXRr5AcaMtex',
        # redirect_uri='http://localhost.ru',
        # grant_type='authorization_code'
)

url = 'https://goga23d.amocrm.ru/api/v4/contacts'
r = oauth.get(url)
print(r.text)



# import requests
# import json

# data = {
#     "client_id": "891a81a8-0e2e-4988-81d6-429a40d98625",
#     "client_secret": "fdwZM6jQsxz66b3aTVpPRmyzY7iZZJxLQoBxwmvPz4eB7pmKQ2xAOXRr5AcaMtex",
#     "grant_type": "authorization_code",
#     "code": "def50200467545482b82f481d233cddc04ef938e13c247e52abef3067bc8022e757aed1b2e803b2bf265e5fa3c2f2f842b46577a91a09ecd5a5a2bee7e79b1428406ddbd5315592a386a1d5c8d521fcaac3bd6767fed4ffbe8d6efb6e4773304720abb602a18c086fb3e20f8c053079924996517bd00924150eda77b0d7db307c0b9e92641c981cd983bd6841c78a1d8ef44da0bb14523fff569ff566bd279095ef10708df4af86241feb3f4305d518f9819d24ed0024539637f33f13f924e1265ddb6ac6caca995618e80cfbc24f8e1ff8f25976acfa62738b4a53b5a5637f8b37ac2c1c017c1769dc93a129dc503284189c66ae1d4165f0337445689814f69ee24a21ecf0d0a018de93d76f4bf614096f69666055c7d14eb151e50d47eb9afc7cc70d5e59025f932be9ed4a8e18100e57833c93bf749472fff1007f63ed91242a7cb8046cfc1ef70a20e007c3dea8c303395be17c0f098d1d392d3ea6938091828914fd10a8351e1b1c8910d77e97cfe3a34baa9dc8e4b7f7806a22f96a457a7302ac0271a27f8966dcf33e2394bade2d05b8ddcf3c8f704fe638398e422ef2089fa6edeec402ddf87a7d62ffd6dbe73b1cdd0ac52034640c21c1829",
#     "redirect_uri": "http://localhost.ru"
# }

# r = requests.post("https://goga23d.amocrm.ru/oauth2/access_token", data=data)
# r_text = json.loads(r.text)

# access_token = r_text['access_token']


# print(r_text)
