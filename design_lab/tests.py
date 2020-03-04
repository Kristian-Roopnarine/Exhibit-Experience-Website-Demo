from django.test import TestCase
from .models import Activities,ActivityLog,Notes,Visitation,Weekend
from datetime import date,datetime

# Create your tests here.

class ActivityTestCase(TestCase):

    def setUp(self):
        Activities.objects.create(name = "Dowels",grade_range = "All",runnable=True)
        Activities.objects.create(name= "Shadow Stories", grade_range="5th +",runnable = False)
        Activities.objects.create(name="Bots",grade_range="5th +",runnable=False)

    def test_manager_query_to_return_runnable_list(self):
        """ Tests the models.Manager query to return all runnable activities"""

        run = Activities.runnable_list.runnable()
        expected_name ="Dowels"
        self.assertEqual(run[0].name,expected_name)

class NoteTestCase(TestCase):
    #return only weekend notes model manager
    #return weekday notes only using manager
    #return notes that show

    def setUp(self):
        Notes.objects.create(description="Only Weekday.",date_added=datetime.today(),weekday=True,weekend=False,show=True,priority=6)

        Notes.objects.create(description="Only Weekend.",date_added=datetime.today(),weekday=False,weekend=True,show=True,priority=6)

        Notes.objects.create(description="Shown is False.",date_added=datetime.today(),weekday=True,weekend=False,show=False,priority=6)

    def test_for_only_weekday_using_manager(self):
        """ Tests the weekday model manager to ensure query set only contains weekday notes."""
        weekday_notes = Notes.weekday_notes.get_weekday_notes()
        expected_description = "Only Weekday."
        self.assertEqual(weekday_notes[0].description,expected_description)
    
    def test_for_only_weekend_using_manager(self):
        """ Tests the weekend model manager to ensure query set only contains weekend notes."""

        weekend_notes = Notes.weekend_notes.get_weekend_notes()
        expected_description = "Only Weekend."
        self.assertEqual(weekend_notes[0].description,expected_description)


    def test_for_not_shown_notes(self):
        """ Tests for notes with shown = False. This query set should only have two items."""

        shown_notes = Notes.objects.filter(show=True)
        self.assertEquals(len(shown_notes),2)


class VisitationTestCase(TestCase):

    def test_return_monday_to_friday_on_weekend(self):
        """ Tests the weekday manager to return monday-friday dates to display activities, and only query max 5 items."""

        #saturday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,11))
        #friday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,10))
        #thursday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,9))
        #wedesnday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,8))
        #tuesday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,7))
        #monday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,6))

        # Jan 11th 2020
        visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
        #should return monday as Jan 6th and friday as Jan 10th
        monday_date = visitor_info_range[0].current_date
        friday_date = visitor_info_range[4].current_date

        expected_monday_date = date(2020,1,6)
        expected_friday_date = date(2020,1,10)
        self.assertEqual(monday_date,expected_monday_date)
        self.assertEqual(friday_date,expected_friday_date)
        self.assertEqual(len(visitor_info_range),5)

    def test_returning_monday_date_on_monday(self):
        """ Testing the query set when it's monday. Should only return 1 item."""

        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,6))
        visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
        self.assertEqual(len(visitor_info_range),1)


    def test_returning_monday_to_wednesday(self):
        """ Testing returning monday-wednesday dates."""

        #wedesnday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,8))
        #tuesday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,7))
        #monday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,6))

        visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
        monday_date = visitor_info_range[0].current_date
        wednesday_date = visitor_info_range[2].current_date
        expected_monday_date = date(2020,1,6)
        expected_wednesday_date = date(2020,1,8)
        self.assertEqual(len(visitor_info_range),3)
        self.assertEqual(monday_date,expected_monday_date)
        self.assertEqual(wednesday_date,expected_wednesday_date)

    def test_returning_monday_to_friday(self):
        """Testing to return monday-friday dates."""

        #friday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,10))
        #thursday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,9))
        #wedesnday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,8))
        #tuesday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,7))
        #monday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,6))

        visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
        monday_date = visitor_info_range[0].current_date
        friday_date = visitor_info_range[4].current_date
        expected_monday_date = date(2020,1,6)
        expected_friday_date = date(2020,1,10)
        self.assertEqual(len(visitor_info_range),5)
        self.assertEqual(monday_date,expected_monday_date)
        self.assertEqual(friday_date,expected_friday_date)
    
    def test_return_activities_monday(self):
        """ Testing the parse_visitor_queryset method"""

        Activities.objects.create(name="Dowels",grade_range="All",runnable=True)
        Activities.objects.create(name="Bots",grade_range="All",runnable=True)
        Activities.objects.create(name="Ziplines",grade_range="All",runnable=True)
        Activities.objects.create(name="Pick It Up",grade_range="All",runnable=True)


        #monday
        Visitation.objects.create(groups ="K - 12th",total_numbers = 100,current_date=date(2020,1,6),sandbox_activity=Activities.objects.get(name="Dowels"),backstage_activity=Activities.objects.get(name="Bots"),treehouse_activity=Activities.objects.get(name="Ziplines"),
        studio_activity=Activities.objects.get(name="Pick It Up"))

        visitor_info_range = Visitation.monday_to_friday.weekday_visitation()
        monday_date = visitor_info_range[0].current_date
        expected_monday_date = date(2020,1,6)
        a = Visitation.parse_visitor_queryset(visitor_info_range)
        expected_a_monday = ['Dowels','Bots','Ziplines','Pick It Up']
        expected_a_friday = []
        self.assertEqual(monday_date,expected_monday_date)
        self.assertEqual(a['Monday'],expected_a_monday)
        self.assertEqual(a['Friday'],expected_a_friday)
