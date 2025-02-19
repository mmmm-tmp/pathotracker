"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

from . import settings
from django.conf.urls.static import static
# from django.views import static ##
# from django.conf import settings ##
#from django.views.static import serve
#from django.conf.urls import url ##

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.post),  # , name='upload'
    path('upload_tree/', views.post_tree),  # , name='upload'
    path('index/', views.home),
    path('', views.index, name='index'),
    path('Tutorial/', views.Tutorial),
    # path('Contact/', views.Contact),
    path('Disclaimer/', views.Disclaimer),
    path('About_Contact/', views.About_Contact),
    path('CRE_network/', views.CRE_network),
    path('PathoTracker/', views.PathoTracker),
    
    path('PathoTracker_ST11/', views.PathoTracker_ST11),
    path('upload_ST11/', views.post_ST11),
    path('ST11_waiting_page/<filename>/', views.waiting_page_ST11),
    path('ST11_waiting/', views.waiting_ST11),
    path('ST11_result/<filename>/', views.result_ST11),
    
    path('wrong/', views.Wrong),
    path('result/<filename>/', views.result),
    path('waiting_page/<filename>/', views.waiting_page),
    path('waiting/', views.waiting),
    
    path('phylogenetic_tree/', views.phylogenetic_tree),
    path('tree_waiting_page/<pathname>/', views.tree_waiting_page),
    path('tree_waiting/', views.tree_waiting),
    path('tree_result/<pathname>/', views.tree_result),
    path('tree_result_download/<pathname>/', views.tree_result_download),
    path('test_sequence/', views.test_sequence),
    path('test_sequence_CMg/', views.test_sequence_CMg),
    path('join_cre/', views.join_cre),
    path('species/', views.species),
    path('post_species/', views.post_species),
    path('species_waiting_page/<filename>/', views.species_waiting_page),
    path('species_waiting/', views.species_waiting),
    path('result_species/<filename>/', views.result_species),
    #path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]+ static(settings.STATIC_URL)


