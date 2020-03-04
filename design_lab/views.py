from django.shortcuts import render
from .models import Activities,Notes,Visitation,ActivityLog,Weekend
from datetime import date,datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist
from .forms import ActivityForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from design_lab.management.commands._services import isWeekday
# Create your views here.

# Below is the first iteration of the website. The refactored code is shown below

"""
def index(request):
    try:
        latest_entry = Visitation.objects.latest('current_date')
    except:
        #create dummy entry
        v = Visitation(groups='Dummy entry',current_date=date.today()-timedelta(1),total_numbers=0)
        v.save()
        latest_entry = v
    
    todays_date = date.today()
    
    try:
        if services.weekdays[todays_date.weekday()] in services.weekdays:
            weekday_range = todays_date.weekday()

            #get the starting day
            end_date = todays_date - timedelta(days = weekday_range)

            #get activity data up to Monday
            weekday_activity = Visitation.objects.filter(current_date__range = [end_date,todays_date]).order_by('current_date')

            #turn into a dictionary of lists
            activities = {'Monday':[],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[]}

            for weekday in weekday_activity:
                activities[services.weekdays[weekday.current_date.weekday()]].extend([weekday.sandbox_activity,weekday.backstage_activity,weekday.treehouse_activity,weekday.studio_activity])
            context['activities'] = activities
    except IndexError:
        print('it is a weekend')
        
    
        #if weekend
        weekday_activity = Visitation.objects.filter(current_date__range = [end_date,todays_date]).order_by('current_date')

        #turn into a dictionary of lists
        activities = {'Monday':[],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[]}

        for weekday in weekday_activity:
            activities[services.weekdays[weekday.current_date.weekday()]].extend([weekday.sandbox_activity,weekday.backstage_activity,weekday.treehouse_activity,weekday.studio_activity])
    
    if request.method == 'GET':
        activity_form = ActivityForm()

    #if design lab activity form was filled out
    if request.method == 'POST':
        edit_entry = Visitation.objects.get(current_date=todays_date)
        activity_form = ActivityForm(request.POST,instance=edit_entry)
        if activity_form.is_valid():
            edit_entry.save()
            return HttpResponseRedirect(reverse("index"))

    #is there an entry in the db for todays date?
    if latest_entry.current_date == todays_date:
        groups = latest_entry.groups
        total = latest_entry.total_numbers
        print('Found entry for todays date')
    else:
        print("Did not find entry for today. Let's check gmail.")
        # if there is no attachment to pull data from
        if services.get_information() == "Could not get group numbers for today.":
            groups = "No group range for today."
            total = "No total numbers for today."
        else:
            cd,gr,t = services.get_information()
            print("Found an automated email, let's check if it corresponds to todays date.")
            
            #sucessfully pulled information from automated email
            if cd == todays_date:
                v = Visitation(groups=gr,current_date=cd,total_numbers=t)
                v.save()
                latest_entry = Visitation.objects.latest('current_date')
                groups = latest_entry.groups
                total = latest_entry.total_numbers
            else:
                groups = "No group numbers for today."
                total = "No total numbers for today."

    activities_list = Activities.objects.filter(runnable=True)
    if not activities_list:
        activities_list = 0

    weekday_notes = Notes.objects.filter(weekday=True,show=True).order_by('-priority','-date_added')
    if not weekday_notes:
        weekday_notes = 0

    weekend_notes = Notes.objects.filter(weekend=True,show=True).order_by('-priority','-date_added')
    if not weekend_notes:
        weekend_notes = 0
        
    weekend_activities = WeekendActivities.objects.latest('date_decided')
    if not weekend_activities:
        weekend_activities= 0

    context = {'total':total,'todays_date':todays_date,'activities_list':activities_list,'weekday_notes':weekday_notes,'weekend_notes':weekend_notes,'weekend_activities':weekend_activities,'groups':groups,'activity_form':activity_form}

    return render(request,'test_app/index.html',context)
    """


def index(request):
    #check if it is a weekday
    context = {}
    todays_date = date.today()
    context['todays_date'] = todays_date

    #check if its a weekday

    try:
        #todays_entry = Visitation.objects.get(current_date=todays_date) # get returns a single query object
        
        context['groups'] = "I developed an algorithm to generate a grade range from an excel sheet containing school grades."
        context['total'] = "We get these numbers from a Gmail API script!"
    except ObjectDoesNotExist:
        # gmail api didn't work
        # its a weekend
        context['groups'] = "It's a weekend! We should only have general admission"
        context['total'] = "Familiessssss"


    """ Old algorithm to display total numbers. 
    The new gmail api algo creates an empty entry on weekdays where there is no data!


    if days_of_week.isWeekday():
        print("It is a weekday!")
        last_entry = Visitation.last_entry.get_today()
        print(Visitation.objects.all())
        print("Let's see if we can find information about todays visitation in our database.")
        
        #check the last entry in the database
        if last_entry.current_date == todays_date:
            print("There is an entry for todays date! Let's show it to you.")
            #if there is an entry found then pull that information
            context['groups'] = last_entry.groups
            context['total'] = last_entry.total_numbers
        else:
            print("There was no entry in the database for today. Let's check the last gmail attachment.")
            #last entry did not match todays date
            #go into gmail to find last email
            cd,gr,t = services.get_information()
            print("Found the attachment. Let's double check to see if it's for todays date.")

            # check if the attachment date match todays date
            if cd == todays_date:
                print("The attachment is for today! Let's save this into the database.")
                v = Visitation(groups=gr,current_date=cd,total_numbers=t)
                v.save()
                last_entry = Visitation.last_entry.get_today()
                context['groups'] = last_entry.groups
                context['total'] = last_entry.total_numbers

            #it is a weekday but no group visitation
            else:
                print("The attachment does not match todays date. That probably means there are no groups today.")
                context['groups'] = "No groups today!"
                context['total'] = "No groups today!"
    
    else:
        print("It's a weekend!")
        context['groups'] ="It's a weekend!"
        context['total'] = "Families"
    """
    #form
    if request.method == 'GET':
        #create activity form
        context['activity_form'] = ActivityForm()

    #if design lab activity form was filled out
    if request.method == 'POST':
        edit_entry = Visitation.objects.get(current_date=todays_date)
        activity_form = ActivityForm(request.POST,instance=edit_entry)
        if activity_form.is_valid() and isWeekday():
            print("The activities were saved into the database.")
            edit_entry.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            context['error'] = "This form is meant to be filled out during the weekdays!"
    
    
    #information to get

    #weekend activities
    print("Getting weekend activities")
  
    try:
        context['weekend_activities']= Weekend.objects.latest('date_decided')
    except ObjectDoesNotExist:
        context['weekend_activities'] = "Pick activities to run for the weekend!"

    #notes
    print("Getting notes for the weekdays and weekend.")
    context['weekday_notes'] = Notes.weekday_notes.get_weekday_notes()

    context['weekend_notes'] = Notes.weekend_notes.get_weekend_notes()

    #runnable activities
    print("Getting a list of runnable activities.")
    context['activities_list'] = Activities.runnable_list.runnable()

    """Weekday activities"""
    #get mondays date for weekday activties
    print("Generating list of activities that were run this week.")
    
    #get visitor information from monday- friday
    visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
    #convert visitor information to dict
    print("Found the days. Converting that information into a dictionary to be viewed.")

    context['activities'] = Visitation.parse_visitor_queryset(visitor_info_range)



    return render(request,"design_lab/index.html",context)

