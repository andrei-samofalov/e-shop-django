from django.core.management import BaseCommand

from purchase.models import DeliveryType


class Command(BaseCommand):
    def handle(self, *args, **options):
        # PaymentType.objects.create(type='Own card')
        # PaymentType.objects.create(type="Someone's card")

        DeliveryType.objects.get_or_create(type='regular', cost=200)
        DeliveryType.objects.get_or_create(type='express', cost=700)

        # OrderStatus.objects.create(type='Accepted')
        # OrderStatus.objects.create(type='Paid')
        # OrderStatus.objects.create(type='Delivered')

        self.stdout.write(self.style.SUCCESS('Basic purchase types created'))
