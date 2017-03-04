from django import forms

from .models import MysqlCluster
class MysqlClusterForm(forms.ModelForm):

    class Meta:
        model = MysqlCluster
        fields = ['name', 'numofnodes', 'ips']