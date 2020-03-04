from django.forms import ModelForm
from design_lab.models import Visitation


class ActivityForm(ModelForm):

    class Meta:
        model = Visitation
        fields = ['sandbox_activity','backstage_activity','studio_activity','treehouse_activity']
