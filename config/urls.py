
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views
from accounts.views import ingredientView, searchView, get_ingredientId, get_match_recipe
from django.conf import settings
from accounts import models
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("recipes/", views.RecipeListView.as_view(), name="recipes"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('add-recipes/', views.RecipeCreateView.as_view(), name="recipes-create"),
    path('recipes/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
    path('recipes/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path('recipes-user', views.UserRecipeView.as_view(), name="user-recipes"),
    

    path('', include('accounts.urls')),
     
    #view 
    path('', ingredientView),
    path('search/<int:ingredientId>/', searchView),

    #api
    path('api/ingredient_id/<ingredientName>', get_ingredientId),
    path('api/match_recipe/', get_match_recipe),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
