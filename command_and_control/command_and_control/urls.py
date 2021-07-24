from django.urls import include, path

urlpatterns = [
    path('instances/', include('web_app.urls')),
    path('tests/', include('web_app.urls'))
]