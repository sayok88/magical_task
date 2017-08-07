
from django.conf.urls import url,include
from rest_framework import routers
from . import views,restview
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

router = routers.DefaultRouter()
router.register(r'employees',views.EmployeeViewSet)
router.register(r'companies',views.CompanyViewSet)
router.register(r'locations',views.LocationViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.elogin, name='login'),
    url(r'^logout/', views.logout1, name='logout'),
    url(r'^addemployee/', views.addemployee, name='addemp'),
    url(r'^addjob/', views.addjob, name='addjob'),

    url(r'^register/', views.register, name='register'),
    url(r'^searchapi/',restview.SearchView.as_view(),name='search'),
    url(r'^api/', include(router.urls)),]