from django import forms

from .models import EtcdCluster

class EtcdClusterForm(forms.ModelForm):

    class Meta:
        model = EtcdCluster
        fields = ['name', 'numofnodes', 'ips']