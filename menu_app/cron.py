from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from .models import Dish


def mail_to_users():
    """Function sending emails with new or updated dishes drom the previous day"""
    yesterday = date.today() - timedelta(days=1)
    new_dishes = Dish.objects.filter(creation_date__contains=yesterday)
    updated_dishes = Dish.objects.filter(last_modified_date__contains=yesterday)
    message = ""
    if new_dishes:
        new_dish_names = ", ".join([dish.name for dish in new_dishes]).lower()
        message += f"Ostatnio dodane przepisy: {new_dish_names}. \n"
    if updated_dishes:
        updated_dish_names = ", ".join([dish.name for dish in updated_dishes]).lower()
        message += f"Ostatnio zmienione przepisy: {updated_dish_names}. \n"
    subject = "Zmiany w menu!"
    from_email = "test@example.com"
    recipients = []
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        recipients.append(user.email)
    email = EmailMessage(subject=subject, body=message, to=recipients)
    if new_dishes or updated_dishes:
        email.send(fail_silently=False)
