from django.core.management.base import BaseCommand
from . import _report_functions
from . import _services
import pandas as pd

"""
This file is a management command that will allow python to automatically create the reports at the end of every month.
"""

class Command(BaseCommand):

    def handle(self,*args, **options):

        run_act,not_run_act,unrunnable_act,lowest,highest,average,beg_date=_report_functions.get_all_data_for_month()
        act,not_run,unrun_act=_report_functions.convert_to_activity_dict(run_act,not_run_act,unrunnable_act)
        stats = _report_functions.convert_to_stat_dict(lowest,highest,average)
        dfs = _report_functions.convert_to_df(act,not_run,unrun_act,stats)
        _services.connect_to_drive(dfs,beg_date)
        