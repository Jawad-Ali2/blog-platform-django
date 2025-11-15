from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post


@receiver(post_save, sender=Post)
def notify_on_publish(sender, instance, created, **kwargs):
    """Send notification when a post is published"""
    if not created and instance.status == 'published':
        # Check if status was changed to published
        old_instance = Post.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.status != 'published':
            # Send notification (in production, you would send actual emails)
            print(f"Notification: Post '{instance.title}' by {instance.author.username} has been published!")
            
            # Example email notification (configure email settings in production)
            # send_mail(
            #     subject=f'New Post Published: {instance.title}',
            #     message=f'{instance.author.username} has published a new post: {instance.title}',
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=['admin@example.com'],
            #     fail_silently=True,
            # )
