from django.core.management.base import BaseCommand
from django.apps import apps
from design_lab.models import ActivityLog,Activities,Visitation
from datetime import date
from ._services import get_information,isWeekday

"""
This is a management command that will be run everyday.
Checks the current date, and the last entry for NYSCIs visitation.
If there is no entry for today, then the function will attempt to get the latest email from Outbound.
If there is no email found, creates an empty entry for today.
If there is an email for today that isn't recorded, it'll create that record.
If the emails date does not match todays date, it defaults to generated information.
"""


class Command(BaseCommand):

    def handle(self,*args,**options):
        latest_entry = Visitation.objects.latest('current_date')
        todays_date = date.today()

        if latest_entry.current_date == todays_date:
            print("Already have an entry for today.")

        else:
            print("No entry for today. getting information")
            cd,gr,t = get_information()
            if cd == todays_date:
                print('Found the email. Saving the information into DB.')
                v = Visitation(groups=gr,total_numbers=t,current_date=cd)
                print(v)
                v.save()
            elif cd != todays_date and isWeekday():
                # no groups today
                print("The last attachment doesn't match todays date. That means we have no groups today.")
                v = Visitation(groups="No Groups Today",total_numbers=0,current_date=todays_date)
                print(v)
                v.save()
            else:
                print("It's a weekend!")
    