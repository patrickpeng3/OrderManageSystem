from django import forms
from cmdb_auth.models import user_auth_cmdb, auth_group


class cmdb_from(forms.ModelForm):
    enable = forms.TypedChoiceField(
        coerc=lambda x: x == 'True',
        choices=((True, '启用'), (False, '禁用')),
        required=True, initial=True,
        widget=forms.RadioSelect,
        label=u"是否启用"
    )

    class Meta:
        model = auth_group
        fields = ["group_name", "explanation", "enable"]


class auth_add_user(forms.ModelForm):
    class Meta:
        model = auth_group
        fields = ["group_user"]


class auth_add(forms.ModelForm):

    class Meta:
        model = user_auth_cmdb

        fields = ['__all__']
