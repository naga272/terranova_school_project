"""
URL configuration for terranova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import home, profile, cambia_stato_ferie
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class SafeLoginView(auth_views.LoginView):
    @method_decorator(ratelimit(key='ip', rate='20/m', block=True))
    @method_decorator(ratelimit(key='post:username', rate='5/m', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),

    # sistema login / logout
    path('login/', SafeLoginView.as_view(template_name="login.html", next_page="profile"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # sistema recupero password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', profile, name="profile"),
    path('cambia_stato_ferie/', cambia_stato_ferie, name="cambia_stato_ferie"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
