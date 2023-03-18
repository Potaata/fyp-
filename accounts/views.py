from django.shortcuts import  render, redirect, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import models
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.template import RequestContext

class HomePageView(TemplateView):
	template_name = 'home.html'

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

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
     context = {
          'recipes' : recipes
     }
     return render(request, "recipes.html", context)
     

@login_required()
def profile(request):
     return render(request, "profile.html")

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')

class RecipeListView(ListView):
     model = models.Recipe
     template_name = 'recipes.html'
     context_object_name = 'recipes'

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
    

class RecipeCreateView(LoginRequiredMixin, CreateView):
     model = models.Recipe
     fields = ['recipe_name', 'photo', 'ingredients', 'servings', 'estimated', 'description']
     template_name = 'add_recipe.html'

     def form_valid(self, form):
          form.instance.author = self.request.user
          return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = models.Recipe
     fields = ['recipe_name', 'ingredients', 'servings', 'estimated', 'description']
     template_name = 'add_recipe.html'

     def test_func(self):
      recipe = self.get_object()
      return self.request.user == recipe.author
    
     def form_valid(self, form):
          form.instance.author = self.request.user
          return super().form_valid(form)
     
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     model = models.Recipe
     success_url = reverse_lazy('recipes')
     template_name = 'recipe_delete.html'

     def test_func(self):
      recipe = self.get_object()
      return self.request.user == recipe.author




def ingredientView(request):
    all_ingredients = models.Ingredients.objects.all()
    return render(request, 'ingredient.html', {'all_ingredients': all_ingredients})

#view for search recipe page
def searchView(request, ingredientId):
    all_recipes= recipeItem.objects.all()
    ingredientObject = ingredientItem.objects.get(id = ingredientId)
    payload = [ingredientObject.name]
    list_recipes = []
    for i in range(0, len(all_recipes)):
      names = []
      ingredients = all_recipes[i].list_ingredient.all()
      for j in range(0, len(ingredients)):
        names.append(ingredients[j].name)
      if set(payload).issubset(set(names)):
        list_recipes.append({'name': all_recipes[i].name,
        'ingredients': all_recipes[i].ingredients.split('#'),
        'directions': all_recipes[i].directions.split('#'),
        'img_url': all_recipes[i].img_url})
    return render(request, 'searchRecipe.html',
    {'ingredientObject': ingredientObject,
    'all_recipes': all_recipes,
    'list_recipes' : list_recipes})
	
	#get ingredient id
def get_ingredientId(request, ingredientName):
  if request.method == 'GET':
    try:
        ingredientId = ingredientItem.objects.get(name = ingredientName).id
        response = json.dumps([{'ingredientId': ingredientId}])
    except:
        response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')

#get match recipes by list of ingredients
@csrf_exempt
def get_match_recipe(request):
  if request.method == 'POST':
    payload = json.loads(request.body).get('listIngredient')
    try:
      all_recipes = recipeItem.objects.all()
      response = []
      for i in range(0, len(all_recipes)):
        names = []
        ingredients = all_recipes[i].list_ingredient.all()
        for j in range(0, len(ingredients)):
          names.append(ingredients[j].name)
        if set(payload).issubset(set(names)):
          response.append({'name': all_recipes[i].name,
          'ingredients': all_recipes[i].ingredients.split('#'),
          'directions': all_recipes[i].directions.split('#'),
          'img_url': all_recipes[i].img_url})
      response = json.dumps(response)
    except:
      response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')
