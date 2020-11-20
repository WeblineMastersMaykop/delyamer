import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import os.path
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from orders.models import Order


def sync_1c():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger_path = os.path.join(os.path.dirname(__file__), 'logs', 'orders_1c.log')
    #logger_path = 'E:\\Goga\\PycharmProjects\\delyamer\\core\\sync\\logs\\orders_1c.log'
    handler = logging.FileHandler(logger_path, 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d.%m.%y %H:%M:%S'))
    logger.addHandler(handler)
    logger.info('НАЧАЛО СКРИПТА')

    current_datetime = timezone.now()
    #path = 'C:\\Users\\gurge\\Desktop\\sync\\orders'
    path = '/home/ftp_delyamer/sync_files/orders'

    old_orders = Order.objects.filter(status__in=('new', 'error'), created__lt=current_datetime-timedelta(days=1)).exclude(pay_type='credit')
    old_orders.update(status='canceled')

    orders = Order.objects.filter(sync_1c=False, status__in=('paid', 'paiding'))
    logger.info('Заказов для выгрузки: {}'.format(len(orders)))

    if orders:
        root = ET.Element('Orders')

        for order in orders:
            order_key = ET.SubElement(
                root,
                'Order',
                attrib={
                    'ID': str(order.id),
                    'Date': order.created.strftime('%d:%m:%Y %H:%M:%S'),
                    'Amount': str(order.total_price),
                    'AmountWithSale': str(order.total_price_with_sale),
                    'Delivery': str(order.get_delivery_display()) if order.delivery else '',
                    'DeliveryPrice': str(order.delivery_price),
                    'TrackNumber': order.track_number or '',
                }
            )

            user_key = ET.SubElement(
                order_key,
                'Customer',
                attrib={
                    'ID': str(order.user.id) if order.user else '',
                    'Name': order.full_name,
                    'Tel': order.phone,
                    'Email': order.email,
                    # 'Postcode': order.postcode,
                    'Country': order.country,
                    'Region': order.region,
                    'City': order.city,
                    'MicroDistrict': order.micro_district,
                    'Street': order.street,
                    'HouseNumber': order.house_nmb,
                    'BuildingNumber': order.building_nmb,
                    'RoomNumber': order.room_nmb,
                }
            )

            payment_key = ET.SubElement(
                order_key,
                'Payment',
                attrib={
                    'Amount': str(order.total_price_with_sale),
                    'Method': str(order.get_pay_type_display()) if order.pay_type else '',
                }
            )

            items_key = ET.SubElement(order_key, 'Products')

            for item in order.items.all().select_related('offer', 'offer__product'):
                product_key = ET.SubElement(
                items_key,
                'Product',
                attrib={
                    'Code': item.offer.product.code_1c,
                    'Name': item.offer.product.name,
                    'Color': item.offer.color.name if item.offer.color else '',
                    'Size': item.offer.size.name if item.offer.size else '',
                    'Cup': item.offer.cup.name if item.offer.cup else '',
                    'Count': str(item.quantity),
                    'Price': str(item.price),
                    'Discount': str(item.discount),
                    'Amount': str(item.total_price_with_sale),
                    'Method': str(item.order.get_pay_type_display()) if item.order.pay_type else '',
                }
            )

        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml()

        file_name = current_datetime.strftime('%d%m%Y%H%M') + '.xml'
        with open(os.path.join(path, file_name), 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        orders.update(sync_1c=True)

    logger.info('КОНЕЦ СКРИПТА\n')


sync_1c()
