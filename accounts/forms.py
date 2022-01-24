# from tkinter import Widget
from django import forms
from .models import Account

# we are using django model forms  for our website

class RegistrationForm(forms.ModelForm):

    #  widget handles  rendering of HTML, and extraction of data from a GET/POST dictionary that corresponds to widget
    password = forms.CharField(widget=forms.PasswordInput(attrs={

            'placeholder': 'Enter Password',
            'class': 'form-control',
            
        })) 

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
            
    })) 

    # meta here brings us innerclass  of accounts we can change order etc from it and use it here using meta class
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def clean(self):

        # The clean() method on a Field subclass is responsible for running to_python() , validate() , and run_validators() in the correct order and propagating their errors. If, at any time, any of the methods raise ValidationError , the validation stops and that error is raised.


        # super is fetching and modifing data of registrationform field
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )
# The __init__.py file is the first file to be loaded in a module, so you can use it to execute code that you want to run each time a module is loaded, or specify the submodules to be exported
    def __init__(self, *args, **kwargs):

        # The Python super() function lets you inherit methods from a parent class
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']= 'Enter Email Address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

