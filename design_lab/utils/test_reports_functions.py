from django.test import TestCase
from . import report_functions
from design_lab.models import ActivityLog,Activities,Visitation
from datetime import date
from collections import Counter


class ActivityDataTestCase(TestCase):
    def setUp(self):
        Activities.objects.create(name="Dowels",grade_range="All",runnable=True)

        Activities.objects.create(name="Bots",grade_range="All",runnable=True)

        Activities.objects.create(name="Ziplines",grade_range="All",runnable=True)

        Activities.objects.create(name="Pegboard Pinball",grade_range="All",runnable=True)

        Activities.objects.create(name="Cardboard City",grade_range="All",runnable=False)

        Activities.objects.create(name="Legos",grade_range="All",runnable=True)

        Visitation.objects.create(groups="All",total_numbers=200,current_date=date(2020,1,1),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        Visitation.objects.create(groups="All",total_numbers=200,current_date=date(2020,1,2),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Pegboard Pinball"))

        Visitation.objects.create(groups="All",total_numbers=280,current_date=date(2020,1,3),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        Visitation.objects.create(groups="All",total_numbers=300,current_date=date(2020,1,4),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        Visitation.objects.create(groups="All",total_numbers=0,current_date=date(2020,1,10),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        Visitation.objects.create(groups="All",total_numbers=450,current_date=date(2020,1,31),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        #december
        Visitation.objects.create(groups="All",total_numbers=550,current_date=date(2019,12,31),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Legos"))

        ActivityLog.objects.create(name=Activities.objects.get(name="Dowels"),
        change="Unrunnable",description="Broke.",
        date_changed=date.today())

        ActivityLog.objects.create(name=Activities.objects.get(name="Dowels"),
        change="Runnable",description="Not Broke.",
        date_changed=date.today())
        
        ActivityLog.objects.create(name=Activities.objects.get(name="Dowels"),
        change="Unrunnable",description="Broke.",
        date_changed=date.today())

    def test_create_month_range(self):
        """ Testing create_month_range to create the 1st and last day of a month."""
        beg_month,month_end_date = report_functions.create_month_range()
        expected_beg_month = date(2020,1,1)
        expected_end_month = date(2020,1,31)
        self.assertEqual(beg_month,expected_beg_month)
        self.assertEqual(month_end_date,expected_end_month)
        
    def test_activity_count_dictionary(self):
        """Tests the generator expression that creates a dictionary of all activities."""

        activity_count = {i.name:0 for i in Activities.objects.all()}
        expected_activity_count = {'Dowels':0,
        'Bots':0,'Ziplines':0,'Legos':0,'Pegboard Pinball':0,'Cardboard City':0}

        self.assertEqual(activity_count,expected_activity_count)

    def test_activity_data(self):
        """ Testing the activity_data function to return activity data during the month of Jan."""
        beg_date,end_date= report_functions.create_month_range()
        run_activities,not_run = report_functions.activity_data(beg_date,end_date)
        expected_run_activities = {'Dowels': 6,
        'Bots':6,"Ziplines":6,"Legos":5,'Pegboard Pinball':1}
        expected_not_run = {'Cardboard City'}
        self.assertEqual(run_activities,expected_run_activities)
        self.assertEqual(not_run,expected_not_run)
    
    def test_number_of_unrunnable_activities(self):
        """ Tests the number_of_unrunnable_activities function. This checks the activity log data."""
        beg_date,end_date= report_functions.create_month_range()
        unrun_dict = report_functions.number_of_unrunnable_activities(beg_date,end_date)
        expected_unrun_dict = {'Dowels':2}
        self.assertEqual(unrun_dict,expected_unrun_dict)
    
    def test_lowest_visitation(self):
        """ Tests that the function returns the lowest visitation for a month that is not zero."""
        beg_date,end_date= report_functions.create_month_range()
        lowest_number = report_functions.lowest_visitation(beg_date,end_date)
        expected_lowest_number = 200
        self.assertEqual(lowest_number,expected_lowest_number)
    
    def test_highest_visitation(self):
        """ Tests whether the function returns the correct highest numbers."""

        beg_date,end_date= report_functions.create_month_range()
        highest = report_functions.highest_visitation(beg_date,end_date)
        expected_highest = 450
        self.assertEqual(highest,expected_highest)
    
    def test_average_visitation(self):
        """ Tests the average_visitation function."""

        beg_date,end_date= report_functions.create_month_range()
        average = report_functions.average_visitation(beg_date,end_date)
        expected_average = 238
        self.assertEqual(average,expected_average)
    
    def test_full_data_function(self):
        """ Testing all functions together."""

        ra,nra,ua,l,h,a = report_functions.get_all_data_for_month()
        expected_ra = {'Dowels': 6,
        'Bots':6,"Ziplines":6,"Legos":5,'Pegboard Pinball':1}
        expected_nra = {'Cardboard City'}
        expected_ua = {'Dowels':2}
        expected_l = 200
        expected_h = 450
        expected_a = 238
        self.assertEqual(ra,expected_ra)
        self.assertEqual(nra,expected_nra)
        self.assertEqual(ua,expected_ua)
        self.assertEqual(l,expected_l)
        self.assertEqual(h,expected_h)
        self.assertEqual(a,expected_a)

def test_convert_to_df_dict(self):
    """ Testing the function to convert the dictionaries to dataframe dictionaries."""

    beg_date,end_date= report_functions.create_month_range()
    run_activities,not_run = report_functions.activity_data(beg_date,end_date)
    expected_run_activities = {'Dowels': 6,
        'Bots':6,"Ziplines":6,"Legos":5,'Pegboard Pinball':1}
    df = report_functions.convert_to_activity_dict(run_activities)
    expected_run_dict = {"Activity Name":['Dowels','Bots','Ziplines','Legos','Pegboard Pinball'],'Number of times run':[6,6,6,5,1]}
    self.assertEqual(run_activities,expected_run_activities)
    self.assertEqual(df,expected_run_dict)
