from django.urls import path
from . import views
from apps.exeat_app.views import apply_for_exeat, list_of_approved_exeat, pending_approved, approve

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('exeatform/', apply_for_exeat.as_view(), name="exeatform"),
    path("approved-exeat/", list_of_approved_exeat, name="list_of_approved_exeat"),
    path("pending_approved/", pending_approved, name="pending_approved"),
    path("approve/<slug:id>", approve, name="approve"),
]