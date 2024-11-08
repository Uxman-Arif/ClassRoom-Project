from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from classroomapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
    path('logout', logoutfnc, name='logout'),
    path('createclass', createclass, name='createclass'),
    path('joinclass', joinclass, name='joinclass'),
    path('get/<int:id>', get_resources, name='get_resources'),
    path('uploadass/<int:id>', upload_assignment, name='upload_assignment'),
    path('assignment/<int:id>', get_assignment, name='get_assignment'),
    path('members/<int:id>', cls_members, name='cls_members'),
    path('stdassignment/<int:id>/<int:stdid>', std_upload_assignment, name='std_assignment'),
    path('instrctrassignment/<int:id>/<int:stdid>', instrctr_see, name='ins_assignment'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
