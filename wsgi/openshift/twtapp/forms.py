from django.forms import Form, CharField, PasswordInput, HiddenInput, Textarea

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
#-------------------------------------------------------------------------------
class SignupForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
#-------------------------------------------------------------------------------

