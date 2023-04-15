
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views
from django.conf import settings
from accounts import models
from django.conf.urls.static import static
from accounts.views import IngredientDeleteView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("profile_list/", views.profile_list, name="profile_list"),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path("update_user/", views.update_user, name="update_user"),
    path("favourites/<int:id>", views.user_favourites, name="user_favourites"),
    path("my_favourites", views.my_favourites, name="my_favourites"),
    path('recipes-user', views.UserRecipeView.as_view(), name="user-recipes"),

    path("about/", views.about, name="about"),
    path("recipes/", views.list_recipe, name="recipes"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('add_recipes/', views.add_recipe, name="recipes-add"),
    path('recipes/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
    path('recipes/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path("search/", views.search, name="search"),   
    path("cocktails", views.cocktail_api, name="cocktails"),
    path("nutrition", views.nutrition_api, name="nutrition"),
    path("admin_approval", views.admin_approval, name="admin_approval"),
    path("ingredients_list/", views.ingredients_list, name="ingredients_list"),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('recipes/<str:sort_by>/', views.list_recipe, name='recipes_sorted'),
    

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset", views.password_reset_request, name="password_reset"),

    path('', include('accounts.urls')),
     
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
