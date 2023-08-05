from django_cron import CronJobBase, Schedule
from django.utils import timezone

from local.models import Local
from renter.models import Payment


class GeneratePaymentsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # every 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'alocation.generate_payments_cron_job'

    def do(self):
        today = timezone.now().date()
        TIME_BETWEEN_PAYMENTS_IN_DAYS = 30

        # get all rented locals
        locals = Local.objects.filter(rented_since__isnull=False)

        for local in locals:
            if local.payment_set.all():
                number_of_days_since_last_payment = (today - local.payment_set.last().created_at).days
                if number_of_days_since_last_payment >= TIME_BETWEEN_PAYMENTS_IN_DAYS:
                    payment = Payment(
                        renter=local.current_tenant,
                        local=local,
                    )

                    # save payment
                    payment.save()




