from django.contrib import admin
from import_export.admin import ExportActionMixin
# Register your models here.

from design_lab.models import Activities,Notes,Visitation,ActivityLog,Weekend


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('name','date_changed','change')

class ActivityLogInline(admin.StackedInline):
    model = ActivityLog
    extra = 0

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name','runnable','grade_range')
    inlines = [ActivityLogInline]

class WeekendActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name','Sandbox','Backstage','Studio','Treehouse')

    def name(self,obj):
        return "Weekend Activities"

class VisitationAdmin(admin.ModelAdmin):
    list_display = ('current_date','total_numbers','groups')

admin.site.register(Activities,ActivitiesAdmin)
admin.site.register(Notes)
admin.site.register(Weekend,WeekendActivitiesAdmin)
admin.site.register(Visitation,VisitationAdmin)
admin.site.register(ActivityLog,ActivityLogAdmin)

