from django.forms import ModelForm, forms, PasswordInput, CharField
from .models import User

class UserForm(ModelForm):

    confirm_password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['name', 'alias', 'email', 'password']
        widgets = {
            'password' : PasswordInput,
        }


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
