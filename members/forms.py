from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Score
from items.models import Item, Sport, ItemCondition
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class UserSignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(UserSignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class ProfileSignUpForm (forms.ModelForm):
    dateofbirth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required = False
    )

    bio = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={
            'class':'form-control', 
            'placeholder':'Write something about yourself...',
            
        }),
        required = False
    )

    class Meta:
        model = Profile
        fields = ("dateofbirth","bio")


class CreateListingForm(forms.ModelForm):
    name = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Item Name'
        })
    )
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    condition = forms.ModelChoiceField(
        queryset=ItemCondition.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Item Description'
        })
    )
    price = forms.FloatField(
        label="", 
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Price (HUF)'
        })
    )

    image = forms.ImageField(
        label="Upload Image", 
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Item
        fields = ('name', 'sport', 'condition', 'description', 'price', 'image')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price cannot be negative. Please enter a valid amount.")
        return price
    
    # def __init__(self):
    #     super(CreateListingForm, self).__init__()
    

class EditListingForm(forms.ModelForm):
    name = forms.CharField(
        label="", 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Item Name'
        })
    )
    sold = forms.BooleanField(
        required=False,
        label="Sold",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    condition = forms.ModelChoiceField(
        queryset=ItemCondition.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Item Description'
        })
    )
    price = forms.FloatField(
        label="", 
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Price (HUF)'
        })
    )

    image = forms.ImageField(
        label="Upload Image (Optional)", 
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Item
        fields = ('name','sold' ,'sport', 'condition', 'description', 'price', 'image')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price cannot be negative. Please enter a valid amount.")
        return price
    

class UserEditForm(UserChangeForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Old Password'})
    )
    new_password1 = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password'})
    )
    new_password2 = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm New Password'})
    )


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }