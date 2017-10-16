from django.conf.urls import url

from .views import logs, reading_list

urlpatterns = [
    url(r"^logs/$", logs, name="reading_logs"),
    url(r"^list/(?P<pk>\d+)/$", reading_list, name="reading_list"),
]
