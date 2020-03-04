from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import date,datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist


BOOL_CHOICES  = (('Unrunnable','Unrunnable'),('Runnable','Runnable'),('Removed','Removed'))


class RunnableAcitivitiesManager(models.Manager):
    def runnable(self):
        activities = Activities.objects.filter(runnable=True)
        if not activities:
            return 0
        else:
            return activities


class Activities(models.Model):
    name = models.CharField(max_length = 50,verbose_name="Name of Activity")
    grade_range = models.CharField(max_length = 50,verbose_name="What grade range is this activity suitable for?")
    runnable = models.BooleanField(default=True,verbose_name="Is this activity runnable?")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Activities'

    runnable_list = RunnableAcitivitiesManager()
    objects = models.Manager()

class WeekdayNotesManager(models.Manager):
    def get_weekday_notes(self):
        try:
            return Notes.objects.filter(weekday=True,show=True).order_by('-priority','-date_added')
        except ObjectDoesNotExist:
            return "No notes found."

class WeekendNotesManager(models.Manager):
    def get_weekend_notes(self):
        try:
            return Notes.objects.filter(weekend=True,show=True).order_by('-priority','-date_added')
        except ObjectDoesNotExist:
            return "No notes found."

class Notes(models.Model):
    description = models.TextField(max_length = 300,verbose_name="Note: ")
    date_added = models.DateTimeField()
    weekday = models.BooleanField(verbose_name="Would you like to show this note during the weekdays?")
    weekend = models.BooleanField(verbose_name="Would you like to show this note during the weekends?")
    show = models.BooleanField(default=True,verbose_name="Do you want to show this note right away?")
    priority = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(6)],verbose_name="How important is this note on a scale of 1-6?")

    def __str__(self):
        return self.description
   

    class Meta:
        verbose_name_plural = 'Notes'
    
    weekday_notes = WeekdayNotesManager()
    weekend_notes = WeekendNotesManager()
    objects = models.Manager()

class VisitationWeekdayManager(models.Manager):
    def weekday_visitation(self):
        today_date = date.today()
        weekday_range = today_date.weekday()
        monday_date = date.today() - timedelta(days=weekday_range)
        friday_date = monday_date + timedelta(4)
        return Visitation.objects.filter(current_date__range = [monday_date,friday_date]).order_by('current_date')


class Visitation(models.Model):
    groups = models.CharField(max_length =100,null=True,verbose_name="Grade Range")
    total_numbers = models.IntegerField(verbose_name="Total Group Numbers")
    current_date = models.DateField()
    sandbox_activity = models.ForeignKey(Activities,on_delete = models.CASCADE,related_name='sandbox',null=True,blank=True)
    backstage_activity = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='backstage',null=True,blank=True)
    treehouse_activity = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='treehouse',null=True,blank=True)
    studio_activity = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='studio',null=True,blank=True)

    @staticmethod
    def parse_visitor_queryset(a_list):
        """ parameters
            a-list: takes in a query set of visitation objects from monday-current date

            Returns a dictionary of Activities ran for each day of the week.
        """
        a = {'Monday':[],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[]}
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for act in a_list:
            try:
                current_day = act.current_date.weekday()
                a[weekdays[current_day]].extend([act.sandbox_activity.name,
                act.backstage_activity.name,
                act.treehouse_activity.name,
                act.studio_activity.name])
                
            except (KeyError,AttributeError) as e: #it's a saturday or sunday or weekday with no activities
                print(e)
                break
        return a


    class Meta:
        verbose_name_plural = 'Museum Group Visitation'
    
    def __str__(self):
        return str(self.current_date)
    
    monday_to_friday = VisitationWeekdayManager()
    objects = models.Manager()
    

class ActivityLog(models.Model):
    name = models.ForeignKey(Activities,on_delete=models.CASCADE)
    change = models.CharField(max_length =15,choices=BOOL_CHOICES,verbose_name="What change are you making to this activity?")
    description = models.CharField(max_length=200)
    date_changed = models.DateField()

    def __str__(self):
        return self.name.name

class Weekend(models.Model):
    Sandbox = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='Sandbox')
    Backstage = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='Backstage')
    Treehouse = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='Treehouse')
    Studio = models.ForeignKey(Activities,on_delete=models.CASCADE,related_name='Studio')
    date_decided = models.DateField(verbose_name="When were the weekend activities decided?")
    
    class Meta:
        verbose_name_plural = 'Weekend Activities'
    
    objects = models.Manager()
