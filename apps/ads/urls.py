from django.urls import path
from .views_html import (
    AdListView, AdDetailView, AdCreateView,
    AdUpdateView, AdDeleteView, ProposalCreateView,
)
from . import views

app_name = "ads"

urlpatterns = [
    path("", AdListView.as_view(), name="ad_list"),
    path("ads/<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("ads/create/", AdCreateView.as_view(), name="ad_create"),
    path("ads/<int:pk>/edit/", AdUpdateView.as_view(), name="ad_edit"),
    path("ads/<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
    path("ads/<int:ad_id>/propose/", ProposalCreateView.as_view(), name="proposal_create"),
    path("proposals/", views.ProposalListView.as_view(), name="proposal_list"),
    path("proposals/<int:pk>/", views.ProposalDetailView.as_view(), name="proposal_detail"),
    path("proposals/<int:pk>/update/", views.ProposalUpdateView.as_view(), name="proposal_update"),
]
