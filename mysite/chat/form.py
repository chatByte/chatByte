from django import forms

# creating a form
class InputForm(forms.Form):

    # first_name = forms.CharField(initial='Your first name', max_length = 200)
    User_name = forms.CharField(max_length = 200)
    # roll_number = forms.IntegerField(
    #                  help_text = "Enter 6 digit roll number"
    #                  )
    Password = forms.CharField(widget = forms.PasswordInput()) 

class CreateAuthorForm(forms.Form):
	User_name = forms.CharField(max_length = 200)
	Github = forms.CharField(max_length = 200)
	Url = forms.CharField(max_length = 200)
	Password = forms.CharField(widget = forms.PasswordInput()) 
