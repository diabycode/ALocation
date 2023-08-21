


from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from local.models import Local
from renter.models import Renter


class Command(BaseCommand):
    help = "Assign locals randomly to renters"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="Number of locals to assign")
        parser.add_argument("--show-details", "-sd", dest="show_details", action="store_true", help="Show more details of proccessing")
        

    def handle(self, *args, **options):
        number = options.get("number")

        unassigned_locals = [l for l in Local.objects.filter(current_tenant=None)][:number]
        renters = [r for r in Renter.objects.all() if r.local_set.all().count() < 2][:number]
        
        for i in range(len(unassigned_locals)):
            renters[i].assign_local(local=unassigned_locals[i])

            if options.get("show_details"):
                self.stdout.write(f"Local '{str(unassigned_locals[i])}' assigned to  renter '{str(renters[i])}'")
        






