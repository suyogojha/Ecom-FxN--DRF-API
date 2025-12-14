from django import forms
from accounts.models import Account



class RegistrarionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']


    # checking password and confirm password same 
    def clean(self):
        cleaned_data = super(RegistrarionForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not Match!!"
            )




    def __init__(self, *args, **kwargs):
        super(RegistrarionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            
            
            