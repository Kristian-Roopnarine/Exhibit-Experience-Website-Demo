from django.test import TestCase
from . import ticket_types

class TicketTypesTestCase(TestCase):

    def test_ticket_filter_generator(self):
        """ Test to ensure list comprehension works."""

        expected_filters = ['pre-k student',
            'k student',
            '1st grade student',
            '2nd grade student',
            '3rd grade student',
            '4th grade student',
            '5th grade student',
            '6th grade student',
            '7th grade student',
            '8th grade student',
            '9th grade student',
            '10th grade student',
            '11th grade student',
            '12th grade student',
            '1st grade student (urban advantage)',
            '2nd grade student (urban advantage)',
            '3rd grade student (urban advantage)',
            '4th grade student (urban advantage)',
            '5th grade student (urban advantage)',
            '6th grade student (urban advantage)',
            '7th grade student (urban advantage)',
            '8th grade student (urban advantage)',
            '9th grade student (urban advantage)',
            '10th grade student (urban advantage)',
            '11th grade student (urban advantage)',
            '12th grade student (urban advantage)',
            '3rd grade student (targeting science)',
            '4th grade student (targeting science)',
            'camp child',
            'student',
            'special needs child',
            'special needs adult',
            'child',
            'group child']
        actual_filters = ticket_types.filters
        self.assertEqual(actual_filters,expected_filters)

    def test_filter_group_range_method(self):
        """ Test to ensure group filtering works."""

        group_range = ['pre-k student',
            'k student',
            '1st grade student',
            '2nd grade student',
            '3rd grade student',
            '4th grade student',
            '12th grade student',
            'child',
            'special needs child',
            'Group adult',
            ]
        
        filtered_group_range = ticket_types.filter_group_range(ticket_types.filters,group_range)
        self.assertNotEqual(group_range,filtered_group_range)

    def test_remap_group_tickets(self):
        """ Testing remap_group_ticket method."""

        filtered_group_range = ['pre-k student',
            'k student',
            '1st grade student',
            '2nd grade student',
            '3rd grade student',
            '4th grade student',
            '12th grade student',
            'child',
            'special needs child',
            'special needs adult'
            ]
        remapped = ticket_types.remap_group_tickets(filtered_group_range,ticket_types.ticket_remap)
        expected_remapped = [0,1,2,3,4,5,13,16,18,18]
        self.assertEqual(remapped,expected_remapped)
    
    def test_order_grade_range_with_all_groups(self):
        """Testing order_grade_range method."""

        remapped = [0,1,2,3,4,5,13,16,18,18]
        grade_range = ticket_types.order_grade_range(remapped,ticket_types.grade_order)
        expected_grade_range= 'Pre K - 12th, Students (Varying Ages) and Special Needs Group.'
        self.assertEqual(grade_range,expected_grade_range)

    def test_order_grade_range_with_no_sorted_special_and_length_longer_than_1(self):
        """ Testing order_grade_range methods logic  only with elementary schools."""

        remapped = [0,4,5,6,1]
        grade_range=ticket_types.order_grade_range(remapped,ticket_types.grade_order)
        expected_grade_range = 'Pre K - 5th'
        self.assertEqual(grade_range,expected_grade_range)

    def test_order_grade_range_with_no_sorted_special_range_and_length_is_1(self):
        """ Testing order_grade_range function with only one grade."""

        remapped = [4]
        grade_range=ticket_types.order_grade_range(remapped,ticket_types.grade_order)
        expected_grade_range = '3rd'
        self.assertEqual(grade_range,expected_grade_range)

    def test_order_grade_range_with_no_range(self):
        """ Testing order_grade_range with no grades."""

        remapped = []
        grade_range=ticket_types.order_grade_range(remapped,ticket_types.grade_order)
        expected_grade_range = "No grade range available."
        self.assertEqual(grade_range,expected_grade_range)

    def test_filter_and_order_group_range(self):
        """ Testing filter_and_order_group_range function."""
        group_range = ['pre-k student',
            'k student',
            '1st grade student',
            '2nd grade student',
            '3rd grade student',
            '4th grade student',
            '12th grade student',
            'child',
            'special needs child',
            'Group adult',
            ]
        ordered_range = ticket_types.filter_and_order_group_range(group_range)
        expected_ordered_range = 'Pre K - 12th, Students (Varying Ages) and Special Needs Group.'
        self.assertEqual(ordered_range,expected_ordered_range)


