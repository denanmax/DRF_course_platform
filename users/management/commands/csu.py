from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='user@user.ru',
            is_staff=False,
            is_superuser=False,

        )
        user.set_password('111')
        user.save()