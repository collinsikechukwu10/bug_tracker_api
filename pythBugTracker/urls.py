from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# Swagger documentation setup
def add_api_documentation_urls():
    schema_view = get_schema_view(
        openapi.Info(
            title="Bug Tracker Project",
            default_version='v1',
            description="API docs for Bug tracker",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="ikechukwu@sankore.com"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    return [
        url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]


urlpatterns = [path('admin/', admin.site.urls),
               # path("auth/", include("core.urls.web")),
               path("api/auth/", include("core.urls.api")),
               # path("bugtracker/", include("bugTracker.urls.web")),
               path("api/bugtracker/", include("bugTracker.urls.api")),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + add_api_documentation_urls()
