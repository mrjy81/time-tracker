from django import forms


class TrackerForm(forms.Form):
    title = forms.CharField(label='Title')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=155)
    password = forms.CharField(max_length=155, widget=forms.PasswordInput)


class EditTrackerTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
