from django.shortcuts import  render, redirect, get_object_or_404
from .forms import NewUserForm, RecipeForm, ProfilePicForm, IngredientForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.views.generic import  ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from .models import Recipe, Ingredients, Profile

from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator 
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def home(request):
      recipes = Recipe.objects.all()
      return render(request, 'home.html',{"recipes":recipes})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = 'django.contrib.auth.backends.ModelBackend' # Set the backend attribute
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('home')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def about(request):
     return render(request, "about.html")

def recipe(request):
     recipes = models.Recipe.objects.all()
     all_ingredients = Recipe.ingredients.all
     return render(request, "recipes.html", {'recipes':recipes, 'all':all_ingredients})
     

@login_required()
def profile(request, pk): 
      if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)
            recipes = Recipe.objects.filter(author_id=pk)
           
            if request.method == "POST":
                  #get current user
                  current_user_profile = request.user.profile
                  #get form data
                  action = request.POST['follow']
                  #follow or unfollow
                  if action == "unfollow":
                        current_user_profile.follows.remove(profile)
                  elif action == "follow":
                        current_user_profile.follows.add(profile)
                    #save profile
                  current_user_profile.save()
            return render(request, "profile.html", {"profile":profile, "recipes":recipes})
      else:
            return redirect('/login')

def logout_request(request): 
    logout(request)
    messages.success(request, ("You have successfully logged out.")) 
    return redirect('/login')

def list_recipe(request): 
     recipe_list = Recipe.objects.all()
     p = Paginator(recipe_list, 6)
     page = request.GET.get('page')
     recipes = p.get_page(page)
     sort_by = request.GET.get('sort_by')
     if sort_by == 'recipe_name':
            recipe_list = recipe_list.order_by('recipe_name')
     elif sort_by == 'recipe_name_desc':
            recipe_list = recipe_list.order_by('-recipe_name')
     elif sort_by == 'created_asc':
            recipe_list = recipe_list.order_by('created_at')
     elif sort_by == 'created_desc':
            recipe_list = recipe_list.order_by('-created_at')
     return render(request, 'recipes.html', {'recipe_list': recipe_list, 'recipes': recipes})

class UserRecipeView(LoginRequiredMixin, ListView):
     model = models.Recipe
     template_name = 'user_recipe.html'
     context_object_name = 'recipes'

     def get_queryset(self):
        return super(UserRecipeView, self).get_queryset().filter(author=self.request.user)

class RecipeDetailView(DetailView):
     model = models.Recipe
     template_name = 'recipe_detail.html'
     is_favourite = False

@login_required   
def add_recipe(request):
      submitted = False
      if request.method == "POST":
          form = RecipeForm(request.POST, request.FILES or None)
          if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()  # save the recipe first
            form.save_m2m()  # save the m2m relationship after saving the form
            return redirect('/recipes')
      else:
            form = RecipeForm()
            if 'submitted' in request.GET:
                submitted=True
      return render(request, "add_recipe.html", {'form':form, 'submitted':submitted})

@login_required  
def add_ingredient(request):
        submitted = False
        if request.method == "POST":
          ingredient_form = IngredientForm(request.POST, request.FILES or None)
          if ingredient_form.is_valid():
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('/ingredients_list')
        else:
            ingredient_form = IngredientForm()
            if 'submitted' in request.GET:
                submitted=True
        return render(request, "ingredients_list.html", {'ingredient_form': ingredient_form, 'submitted':submitted})
     
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = models.Recipe
     fields = ['recipe_name', 'photo', 'ingredients', 'servings', 'estimated', 'description']
     template_name = 'add_recipe.html'

     def test_func(self):
      recipe = self.get_object()
      return self.request.user == recipe.author or self.request.user.is_superuser
    
     def form_valid(self, form):
            recipe = form.save(commit=False)
            form.instance.author = self.request.user
            recipe.save()  # save the recipe first
            form.save_m2m()  # save the m2m relationship after saving the form
            return super().form_valid(form)
     
     
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     model = models.Recipe
     success_url = reverse_lazy('recipes')
     template_name = 'recipe_delete.html'

     def test_func(self):
      recipe = self.get_object()
      return self.request.user == recipe.author or self.request.user.is_superuser

#view for search recipe page
def search(request):
     if request.method == "POST":
          searched = request.POST['searched']
          ingredients = Ingredients.objects.filter(ingredient_name__icontains=searched)
          recipe_ids = Recipe.objects.filter(ingredients__in=ingredients).values_list('id', flat=True)
          recipes = Recipe.objects.filter(Q(recipe_name__contains=searched) | Q(id__in=recipe_ids))
          return render(request, "search.html", {'searched':searched, 'recipes':recipes})
     else:
          return render(request, "search.html",{})

def profile_list(request):
      if request.user.is_authenticated:
          profiles = Profile.objects.exclude(user=request.user).order_by('user')
          return render(request, 'profile_list.html', {"profiles":profiles})
      else:
          return redirect('/login')
      
def update_user(request):
      if request.user.is_authenticated:
       current_user = User.objects.get(id=request.user.id)
       profile_user = Profile.objects.get(user__id=request.user.id)
       
       user_form = NewUserForm(request.POST or None, request.FILES or None, instance=current_user)
       profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
       if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            login(request, current_user)
            return redirect('home')
       return render(request, 'update_user.html', {'user_form':user_form, 'profile_form': profile_form})
      else:
       return redirect('home')

@login_required
def user_favourites(request, id):
      recipe = get_object_or_404(Recipe, id=id )
      if recipe.favourites.filter(id=request.user.id).exists():
            recipe.favourites.remove(request.user)
            messages.success(request, "Recipe has been removed from Favourites")

      else:
            recipe.favourites.add(request.user)
            messages.success(request, "Added to Favourites")
      return redirect('my_favourites')
      

@login_required
def my_favourites(request):
     recipes = Recipe.objects.filter(favourites=request.user)
     return render(request, "favourites.html",{"my_favourites": recipes})

def cocktail_api(request):
    import json
    import requests


    if request.method == 'POST':
        query = request.POST['query']
    # Define the URL of the API endpoint and the data to be sent
        url = 'https://api.api-ninjas.com/v1/cocktail?name='

    # Make the POST request to the API
        response = requests.get(url +query , headers={'X-Api-Key': 'tncg2NmUn3aNAcejOljUNA==GrLMEai3pkDEDoeE'})

    # Check if the request was successful
        try:
        # If successful, process the response content and render a template
            api = json.loads(response.content)
            print(response.content)
        except Exception as e: 
            api = " oops! your requested cocktail was not found."
            print (e)
        return render(request, 'cocktails.html',{'api':api})
    else:

        query = 'bloody mary'
            # Define the URL of the API endpoint and the data to be sent
        url = 'https://api.api-ninjas.com/v1/cocktail?name='

            # Make the POST request to the API
        response = requests.get(url +query , headers={'X-Api-Key': 'tncg2NmUn3aNAcejOljUNA==GrLMEai3pkDEDoeE'})

            # Check if the request was successful
        try:
                # If successful, process the response content and render a template
                    api = json.loads(response.content)
                    print(response.content)
        except Exception as e: 
                    api = " oops! your requested cocktail was not found."
                    print (e)
        return render(request, 'cocktails.html',{'api':api}) 
    

def nutrition_api(request):
    import json
    import requests


    if request.method == 'POST':
        query = request.POST['query']
    # Define the URL of the API endpoint and the data to be sent
        url = 'https://api.api-ninjas.com/v1/nutrition?query='

    # Make the POST request to the API
        response = requests.get(url +query , headers={'X-Api-Key': 'tncg2NmUn3aNAcejOljUNA==GrLMEai3pkDEDoeE'})

    # Check if the request was successful
        try:
        # If successful, process the response content and render a template
            api = json.loads(response.content)
            print(response.content)
        except Exception as e: 
            api = " oops! your requested food was not found."
            print (e)
        return render(request, 'nutrition.html',{'api':api})
    else:

        query = '1lb brisket'
            # Define the URL of the API endpoint and the data to be sent
        url = 'https://api.api-ninjas.com/v1/nutrition?query='

            # Make the POST request to the API
        response = requests.get(url +query , headers={'X-Api-Key': 'tncg2NmUn3aNAcejOljUNA==GrLMEai3pkDEDoeE'})

            # Check if the request was successful
        try:
                # If successful, process the response content and render a template
                    api = json.loads(response.content)
                    print(response.content)
        except Exception as e: 
                    api = " oops! your requested food was not found."
                    print (e)
        return render(request, 'nutrition.html',{'api':api}) 
    
    
def admin_approval(request):
      ingredient_list = Ingredients.objects.all().order_by('ingredient_name')
      recipes = Recipe.objects.all()
      if request.user.is_superuser:
          if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            
            #Uncheck ingredients
            ingredient_list.update(approved=False)

            #Update Database
            for x in id_list:
                 Ingredients.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request, ("Ingredient has been approved."))
            return redirect('ingredients_list') 
          else:
            return render(request, 'admin_approval.html',{"ingredient_list": ingredient_list, "recipes":recipes}) 
      else:
          return redirect('home')      
      

def ingredients_list(request):
        ingredient_list = Ingredients.objects.all()
        submitted = False
        if request.method == "POST":
          ingredient_form = IngredientForm(request.POST, request.FILES or None)
          if ingredient_form.is_valid():
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            return redirect('/ingredients_list')
        else:
            ingredient_form = IngredientForm()
            if 'submitted' in request.GET:
                submitted=True
        return render(request, "ingredients_list.html", {'ingredient_list': ingredient_list, 'ingredient_form': ingredient_form, 'submitted':submitted})


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

class IngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingredients
    success_url = reverse_lazy('admin_approval') # change this to the appropriate success url
    template_name = 'recipe_delete.html'

    def test_func(self):
        ingredient = self.get_object()
        return self.request.user.is_superuser

