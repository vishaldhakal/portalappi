from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import DeveloperListCreateView, DeveloperRetrieveUpdateDeleteView, PreConstructionListCreateView, PreConstructionRetrieveUpdateDeleteView, EventListCreateView, EventRetrieveUpdateDeleteView, NewsListCreateView, NewsRetrieveUpdateDeleteView, FavouriteListCreateView, FavouriteRetrieveUpdateDeleteView, CityListCreateView, CityRetrieveUpdateDeleteView, PreConstructionDetailView, PreConstructionsCityView, delete_image, delete_floorplan, remove_last_part_of_slug, get_all_city, get_related_precons

schema_view = get_schema_view(
    openapi.Info(
        title="API Portal",
        default_version='v1',
        description="Portal Description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="8ba7483e-786c-4ffa-9c2b-0ddd50e82441"),
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('developers/', DeveloperListCreateView.as_view(),
         name='developer-list-create'),
    path('developers/<int:pk>/', DeveloperRetrieveUpdateDeleteView.as_view(),
         name='developer-retrieve-update-delete'),
    path('preconstructions/', PreConstructionListCreateView.as_view(),
         name='preconstruction-list-create'),
    path('preconstructions/<int:pk>/', PreConstructionRetrieveUpdateDeleteView.as_view(),
         name='preconstruction-retrieve-update-delete'),
    path('preconstructions-city/<str:slug>/', PreConstructionsCityView,
         name='preconstruction-city'),
    path('preconstructions-detail/<str:slug>/', PreConstructionDetailView,
         name='preconstruction-retrieve'),
    path('related-precons/<str:city>/',
         get_related_precons, name='related-precons'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-floorplan/<int:pk>/', delete_floorplan, name='delete_floorplan'),
    path('events/<int:pk>/', EventRetrieveUpdateDeleteView.as_view(),
         name='event-retrieve-update-delete'),
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('remove-last-part-of-slug/', remove_last_part_of_slug,
         name='remove-last-part-of-slug'),
    path('news/<int:pk>/', NewsRetrieveUpdateDeleteView.as_view(),
         name='news-retrieve-update-delete'),
    path('city/', CityListCreateView.as_view(), name='city-list-create'),
    path('all-city/', get_all_city, name='get-all-city'),
    path('city/<int:pk>/', CityRetrieveUpdateDeleteView.as_view(),
         name='city-retrieve-update-delete'),
    path('favourites/', FavouriteListCreateView.as_view(),
         name='favourite-list-create'),
    path('favourites/<int:pk>/', FavouriteRetrieveUpdateDeleteView.as_view(),
         name='favourite-retrieve-update-delete'),
]
