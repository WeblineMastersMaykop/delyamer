import xml.etree.ElementTree as ET
import os.path
from sys import exit
import logging
from slugify import slugify
from django.core.files.images import ImageFile
from products.models import Offer, Product, Category, Color, Size, Cup, ProductImage


def sync_1c():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger_path = os.path.join(os.path.dirname(__file__), 'offers_1c.log')
    # logger_path = 'E:\\Goga\\PycharmProjects\\delyamer\\core\\offers_1c.log'
    handler = logging.FileHandler(logger_path, 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d.%m.%y %H:%M:%S'))
    logger.addHandler(handler)
    logger.info('НАЧАЛО СКРИПТА')

    path = 'C:\\Users\\gurge\\Desktop\\sync'

    try:
        tree = ET.parse(os.path.join(path, 'offers.xml'))
    except FileNotFoundError as e:
        logger.error('Файл offers.xml не найден')
        logger.info('КОНЕЦ СКРИПТА\n')
        exit()

    root = tree.getroot()

    for category_key in root.findall('Catalog'):
        # Создание и изменение категорий
        category, created = Category.objects.update_or_create(
            code_1c=category_key.attrib['Code'],
            defaults={
                'name': category_key.attrib['Name'],
                'slug': slugify(category_key.attrib['Name'])
            },
        )

        # Товары с текущей категорией на сайте
        products = Product.objects.filter(category=category, is_active=True)

        logger.info(category)
        # Создание и изменение товаров
        for product_key in category_key:
            product, created = Product.objects.update_or_create(
                code_1c=product_key.attrib['Code'],
                defaults={
                    'category': category,
                    'name': product_key.attrib['NameFull'],
                    'vendor_code': product_key.attrib['Model'],
                    'pushup': int(product_key.attrib['Pushup']),
                    'price': int(product_key.attrib['Price'].split('.')[0] or 0),
                    'is_active': int(product_key.attrib['Active']),
                    'slug': slugify(product_key.attrib['NameFull'] + '-' + str(product_key.attrib['Code']))
                },
            )

            products = products.exclude(code_1c=product_key.attrib['Code'])

            offers = Offer.objects.filter(product=product, is_active=True)

            # Удаляю у товара все картинки и добавляю заново
            ProductImage.objects.filter(product=product).delete()

            for color_key in product_key:
                # Создание и изменение цветов
                color = None
                if color_key.attrib['Name']:
                    color, created = Color.objects.update_or_create(
                        code_1c=color_key.attrib['Code'],
                        defaults={
                            'name': color_key.attrib['Name'].capitalize()
                        },
                    )

                if color_key.attrib['Picture']:
                    product_image = ProductImage.objects.create(
                        product=product,
                        color=color,
                        image=ImageFile(open(os.path.join(path, 'Images', color_key.attrib['Picture']), 'rb'))
                    )

                for parametrs_key in color_key:
                    # Создание и изменение размеров
                    size = None
                    if parametrs_key.attrib['Size']:
                        size, created = Size.objects.get_or_create(
                            name=parametrs_key.attrib['Size']
                        )
                    # Создание и изменение чашек
                    cup = None
                    if parametrs_key.attrib['Cup']:
                        cup, created = Cup.objects.get_or_create(
                            name=parametrs_key.attrib['Cup']
                        )

                    # Считаю сколько осталось на складе
                    stock = 0
                    for balance_key in parametrs_key:
                        stock += int(balance_key.attrib['Count'])

                    # Создание и изменение вариантов товаров
                    offer, created = Offer.objects.update_or_create(
                        product=product,
                        size=size,
                        color=color,
                        cup=cup,
                        defaults={
                            'is_active': True,
                            'stock': stock
                        }
                    )

                    offers = offers.exclude(product=product, size=size, color=color, cup=cup)

            # Варианты товаров, которых нет в выгрузке делаю неактивными
            # for offer in offers:
            #     offer.is_active = False

            # Offer.objects.bulk_update(offers, ['is_active'])
            offers.update(is_active=False)

        # Товары, которых нет в выгрузке делаю неактивными
        products.update(is_active=False)

    logger.info('КОНЕЦ СКРИПТА\n')


# sync_1c()
