from design_lab.models import ActivityLog,Activities,Visitation
from django.db.models import Sum,Avg,Max,Min
import math
from collections import Counter
from datetime import date
import calendar
import pandas as pd


"""
This file contains all the functions that generate the monthly report for Design Lab.
It is to be run as a cron job, and it has an "_" prefix because it is a private module that python will not automatically run.
"""

def create_month_range():
    """ Returns first and last date of the month."""

    this_year = date.today().year
    this_month = date.today().month
    end_month=calendar.monthrange(this_year,this_month)[1]
    beg_date = date(this_year,this_month,1)
    end_date = date(this_year,this_month,end_month)
    return beg_date,end_date

def activity_data(beg_date,end_date):
    """ Returns a_run and diff
    a_run : A dictionary containing all activity names as keys and the amount they were run as values
    diff : A set containing all activities that were not run this month. """

    print("_"*20)
    print("Report testing")
    design_pods = ['sandbox_activity__name','backstage_activity__name','treehouse_activity__name','studio_activity__name']

    #creates a dictionary to count the activities 
    activity_count = {i.name : 0 for i in Activities.objects.all()}
    
    # counts the number of times an activity is run
    a_run = dict(Counter(name[pod] for pod in design_pods for name in Visitation.objects.filter(current_date__range=[beg_date,end_date]).values(pod) if name[pod] != None))
    diff = set(activity_count) - set(a_run)
    return a_run, diff

def number_of_unrunnable_activities(beg_date,end_date):
    """ Returns a dictionary containing all activities that were changed to unrunnnable as keys, and the amount they were switched as values.
    """

    unrunnable_activity_count = [i.name.name for i in ActivityLog.objects.filter(change="Unrunnable").filter(date_changed__range=[beg_date,end_date])]

    return dict(Counter(unrunnable_activity_count))

def lowest_visitation(beg_date,end_date):
    return Visitation.objects.filter(total_numbers__gt=0).aggregate(Min('total_numbers'))['total_numbers__min']

def highest_visitation(beg_date,end_date):
    return Visitation.objects.filter(current_date__range=[beg_date,end_date]).aggregate(Max('total_numbers'))['total_numbers__max']

def average_visitation(beg_date,end_date):
    return math.floor(Visitation.objects.filter(current_date__range=[beg_date,end_date]).aggregate(Avg('total_numbers'))['total_numbers__avg'])

def get_all_data_for_month():
    beg_date,end_date= create_month_range()
    run_act,not_run_act = activity_data(beg_date,end_date)
    unrunnable_act = number_of_unrunnable_activities(beg_date,end_date)
    lowest=lowest_visitation(beg_date,end_date)
    highest = highest_visitation(beg_date,end_date)
    average = average_visitation(beg_date,end_date)
    return run_act,not_run_act,unrunnable_act,lowest,highest,average,beg_date

def convert_to_activity_dict(run_dict,not_run,unrun_dict):
    new_act_dict = {'ACTIVITY NAME':[],'NUMBER OF TIMES RUN IN DL':[]}
    new_not_run = {"ACTIVITIES THAT WERE NOT RUN":[]}
    unrunnable_dict = {'UNRUNNABLE/BROKEN ACTIVITIES':[],"NUMBER OF TIMES SWITCHED FROM RUNNABLE":[]}
    for activity,number in run_dict.items():
        new_act_dict['ACTIVITY NAME'].append(activity)
        new_act_dict['NUMBER OF TIMES RUN IN DL'].append(number)
    for activity in not_run:
        new_not_run["ACTIVITIES THAT WERE NOT RUN"].append(activity)
    for activity,number in unrun_dict.items():
        unrunnable_dict['UNRUNNABLE/BROKEN ACTIVITIES'].append(activity)
        unrunnable_dict['NUMBER OF TIMES SWITCHED FROM RUNNABLE'].append(number)
    return new_act_dict,new_not_run,unrunnable_dict

def convert_to_stat_dict(l,h,a):
    stat_dict = {'GROUP STATISTICS':['Lowest','Highest','Average'],'NUMBER OF GROUPS':[]}
    stat_dict['NUMBER OF GROUPS'].extend([l,h,a])
    return stat_dict

def convert_to_df(ad,nr,ur,st):
    """ Parameters:
        ad: Dictionary of data for the run activities this month
        nr: Dictionary of data for activities not run this month
        ur: Dictionary of unrunnable activities for this month
        st: Dictionary of stats data 
    """
    act_df = pd.DataFrame(data=ad)
    nr_df = pd.DataFrame(data =nr)
    ur_df = pd.DataFrame(data=ur)
    st_df = pd.DataFrame(data=st)
    return act_df,nr_df,ur_df,st_df
