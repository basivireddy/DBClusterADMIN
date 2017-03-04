from django import forms
from .models import CouchCluster


class CouchClusterForm(forms.ModelForm):

    class Meta:
        model = CouchCluster
        fields = ['name', 'numofnodes', 'ips']