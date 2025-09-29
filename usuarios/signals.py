from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    Group.objects.get_or_create(name='Cliente')
    Group.objects.get_or_create(name='Barbero')
    Group.objects.get_or_create(name='AdminLocal')
