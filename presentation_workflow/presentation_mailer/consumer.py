import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

def process_approval(ch, method, properties, body):
    presentation_info = json.loads(body)
    send_mail(
    "Your presentation has been accepted",
    f'{presentation_info["presenter_name"]}, we\'re happy to tell you that your presentation {presentation_info["title"]} has been accepted.',
    f'admin@conference.go',
    [f'{presentation_info["presenter_email"]}'],
    fail_silently=False  
    )
    print("mail sent")

def process_rejection(ch, method, properties, body):
    presentation_info = json.loads(body)
    send_mail(
    "Your presentation was not selected",
    f'{presentation_info["presenter_name"]}, we regret to tell you that your presentation {presentation_info["title"]} was not selected.',
    f'admin@conference.go',
    [f'{presentation_info["presenter_email"]}'],
    fail_silently=False  
    )
    print("mail sent")


while True:
    try:
        print("hello thomas")
        parameters = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='presentation_approvals')
        channel.queue_declare(queue='presentation_rejections')
        channel.basic_consume(
            queue='presentation_approvals',
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.basic_consume(
            queue='presentation_rejections',
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)




