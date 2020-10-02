import os
import os.path
import logging
import requests
import json
from uuid import uuid1
from django.core.files.images import ImageFile
from core.models import InstagramPhotos


def sync():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger_path = os.path.join(os.path.dirname(__file__), 'logs', 'instagram.log')
    # logger_path = 'E:\\Goga\\PycharmProjects\\delyamer\\core\\sync\\logs\\instagram.log'
    handler = logging.FileHandler(logger_path, 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d.%m.%y %H:%M:%S'))
    logger.addHandler(handler)
    logger.info('НАЧАЛО СКРИПТА')

    r = requests.get('https://www.instagram.com/delyamer/?__a=1')
    r_text = json.loads(r.text)

    edges = r_text['graphql']['user']['edge_owner_to_timeline_media']['edges']

    if edges:
        logger.info('Профиль открыт, получаю фотографии')
        InstagramPhotos.objects.all().delete()
    else:
        logger.info('Профиль закрыт')

    for item in edges[:8]:
        r = requests.get(item['node']['display_url'], stream=True)
        r.raw.decode_content = True
        instagram_photo = InstagramPhotos.objects.create(
            image=ImageFile(r.raw, name=str(uuid1())+'.jpg')
        )

    logger.info('КОНЕЦ СКРИПТА\n')


# sync()
