from django import forms

# creating a form
class LoginForm(forms.Form):

    # first_name = forms.CharField(initial='Your first name', max_length = 200)
    Username = forms.CharField(max_length = 200)
    # roll_number = forms.IntegerField(
    #                  help_text = "Enter 6 digit roll number"
    #                  )
    Password = forms.CharField(widget = forms.PasswordInput())

class CreateAuthorForm(forms.Form):
    User_name = forms.CharField(max_length=200)
    Password = forms.CharField(max_length=200)
    Host = forms.CharField(max_length=200)
    Url = forms.CharField(max_length=200)
    GitHub = forms.CharField(max_length=200)
	# Password = forms.CharField(widget = forms.PasswordInput())

class CreatePostForm(forms.Form):
    title = forms.CharField(label=False, widget=forms.Textarea(attrs={'id':'title', 'cols':35, 'rows':1, 'class':'form-title-control', 'placeholder':'Title'}))
    description = forms.CharField(label=False, widget=forms.Textarea(attrs={'id':'description', 'cols':35, 'rows':4, 'class':'form-title-control', 'placeholder':'Description: Anything exciting?'}))
