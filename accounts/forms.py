from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from .models import *

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'


class RecipeForm(ModelForm):
	servings = forms.IntegerField(min_value=1)
	class Meta:
			model = Recipe
			fields = ("recipe_name", "ingredients", 
			"description", "servings", "estimated", "photo")
			labels = {
				'recipe_name':'', 
				'ingredients':'Ingredients',
				
				'description':'', 
				'servings':'Servings', 
				'estimated':'', 
				'photo':'Image',
			}
			widgets = {
				'recipe_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Recipe Name'}),
				'ingredients': forms.CheckboxSelectMultiple(attrs={}),
				'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Instructions'}),
				'servings': forms.NumberInput(attrs={'class':'form-control'}),
				'estimated': forms.TextInput(attrs={'class':'form-control','placeholder':'Estimated Time'}),
			}

	def save(self, commit=True):
			instance = super().save(commit=False)
			return instance

	
class ProfilePicForm(forms.ModelForm):
	profile_image = forms.ImageField(label="Profile Picture")
	
	class Meta:
		model = Profile
		fields = ("profile_image",)
		

class IngredientForm(forms.ModelForm):
	ingredient_name = forms.TextInput
	
	class Meta:
		model = Ingredients
		fields = ("ingredient_name", )
		widgets = {
				'ingredient_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'New Ingredient'}),}



