from django.apps import AppConfig


class CarDealerConfig(AppConfig):
    name = 'car_dealer'

    def ready(self):
        import car_dealer.signals