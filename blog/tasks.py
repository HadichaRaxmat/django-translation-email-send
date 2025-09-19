from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Contact


@shared_task
def send_contact_email(contact_id):
    contact = Contact.objects.get(id=contact_id)

    # 1️⃣ Письмо менеджеру
    subject_manager = f"Новый контакт от {contact.name} ({contact.email})"
    message_manager = f"""
Имя: {contact.name}
Email: {contact.email}
Сообщение:
{contact.message}
"""
    email_manager = EmailMessage(
        subject=subject_manager,
        body=message_manager,
        from_email=settings.EMAIL_HOST_USER,  # твоя почта
        to=[settings.EMAIL_HOST_USER],  # менеджер
        reply_to=[contact.email],  # ответ пойдет пользователю
    )
    email_manager.send(fail_silently=False)

    # 2️⃣ Письмо пользователю (подтверждение)

    subject_user = "Ваше сообщение успешно отправлено"
    message_user = f"Здравствуйте, {contact.name}! Мы получили ваше сообщение и свяжемся с вами в ближайшее время."

    from_email = f"No Reply <{settings.EMAIL_HOST_USER}>"  # твоя Gmail

    email_user = EmailMessage(
        subject=subject_user,
        body=message_user,
        from_email=from_email,  # будет отображаться как No Reply
        to=[contact.email],  # пользователь
        # reply_to не указываем
    )
    email_user.send(fail_silently=False)
    print(f"Письмо пользователю ({contact.email}) отправлено")

