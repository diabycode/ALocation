from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from renter.models import Renter


class Command(BaseCommand):
    help = "Create a specific number of renter"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="Number of renter to generate")
        parser.add_argument("--show-details", "-sd", dest="show_details", action="store_true", help="Show more details of proccessing")
        

    def handle(self, *args, **options):
        number = options.get("number")
        
        fk = Faker(locale="fr-FR")

        # number : 4
        # create 4 number of renter
        for i in range(number):
            last_name = fk.last_name()
            first_name = fk.first_name()
            phone = fk.phone_number()
            address = fk.address()


            renter = Renter(
                last_name=last_name,
                first_name=first_name,
                phone=phone,
                address=address
            )

            renter.save()

            if options.get("show_details"):
                self.stdout.write(last_name + " " + first_name)
                self.stdout.write(phone)
                self.stdout.write(address)
                self.stdout.write("------\n")

        self.stdout.write(f"{number} renter(s) created !")




