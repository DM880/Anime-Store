from django import forms


from store.data.user.models import CustomUser


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=20)
    email = forms.EmailField(label="Email", max_length=200)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


#Used for user creation in appsite
class UserCreate(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'date_of_birth','email', 'password']

