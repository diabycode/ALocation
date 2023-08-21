from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from local.models import Local


class Command(BaseCommand):
    help = "Create a specific number of local"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="Number of local to generate")
        parser.add_argument("--show-details", "-sd", dest="show_details", action="store_true", help="Show more details of proccessing")
        

    def handle(self, *args, **options):
        number = options.get("number")
        
        fk = Faker(locale="fr-FR")

        # number : 4
        # create 4 number of renter
        for i in range(number):
            tag_name = "local_ " + str(fk.random_int(min=1, max=5000)).zfill(5)
            rent_price = fk.random_int(min=5000, max=35000)
            address = fk.address()


            local = Local(
                tag_name=tag_name,
                rent_price=rent_price,
                address=address
            )

            local.save()

            if options.get("show_details"):
                self.stdout.write(tag_name)
                self.stdout.write(str(rent_price))
                self.stdout.write(address)
                self.stdout.write("------\n\n")

        self.stdout.write(f"{number} local(s) created !")









