ticket_remap = {
    'pre-k student':0,
    'k student':1,
    '1st grade student':2,
    '2nd grade student':3,
    '3rd grade student':4,
    '4th grade student':5,
    '5th grade student':6,
    '6th grade student':7,
    '7th grade student':8,
    '8th grade student':9,
    '9th grade student':10,
    '10th grade student':11,
    '11th grade student':12,
    '12th grade student':13,
    '1st grade student (urban advantage)':2,
    '2nd grade student (urban advantage)':3,
    '3rd grade student (urban advantage)':4,
    '4th grade student (urban advantage)':5,
    '5th grade student (urban advantage)':6,
    '6th grade student (urban advantage)':7,
    '7th grade student (urban advantage)':8,
    '8th grade student (urban advantage)':9,
    '9th grade student (urban advantage)':10,
    '10th grade student (urban advantage)':11,
    '11th grade student (urban advantage)':12,
    '12th grade student (urban advantage)':13,
    '3rd grade student (targeting science)':4,
    '4th grade student (targeting science)':5,
    'camp child':17,
    'student':16,
    'special needs child':18,
    'special needs adult':18,
    'child':16,
    'group child':16,
}

grade_order = ['Pre K',
    'K',
    '1st',
    '2nd',
    '3rd',
    '4th',
    '5th',
    '6th',
    '7th',
    '8th',
    '9th',
    '10th',
    '11th',
    '12th',
    'Child/Families (ages 2-17)',
    'Group Child (varying ages)',
    'Students (Varying Ages)',
    'Camps (Varying ages)',
    'Special Needs Group'
]

filters = [a for a in ticket_remap]


def filter_group_range(filters,group_range):
    filtered_group_range = []
    for groups in group_range:
        if groups.lower() in filters:
            filtered_group_range.append(groups)
    return filtered_group_range

def remap_group_tickets(filtered_group,rename):
    # rename filtered group list
    return [rename[x.lower()] for x in filtered_group]

def order_grade_range(group_list,grade_order):
    group_list.sort(key = int)
    sorted_grade_range = [grade_order[x] for x in group_list if x < 14]
    sorted_special_range = [grade_order[x] for x in group_list if x >= 16]

    #check if we have any special needs groups
    if "Special Needs Group" in sorted_special_range:
        special_needs = f' and {grade_order[18]}.'
    else:
        special_needs = ''

    #if there are no special group type tickets
    if len(sorted_special_range) == 0:
        
        #if there are more than one grade range
        if len(sorted_grade_range) > 1:
            return sorted_grade_range[0] + " - " + sorted_grade_range[-1] + special_needs
        elif len(sorted_grade_range) == 1:
            return sorted_grade_range[0] + special_needs
        else:
            return "No grade range available."
    else:
        return sorted_grade_range[0] + " - " + sorted_grade_range[-1] + ", " + sorted_special_range[0] + special_needs

def filter_and_order_group_range(group_range):
    filtered_group = filter_group_range(filters,group_range)
    remapped_names = remap_group_tickets(filtered_group,ticket_remap)
    grade_range = order_grade_range(remapped_names,grade_order)
    return grade_range


