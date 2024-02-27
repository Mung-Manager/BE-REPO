import logging

from django.urls import path

logger = logging.getLogger("configuration")


def show_swagger(*args, **kwargs) -> bool:
    from config.settings.swagger.settings import SWAGGER_ENABLED

    if not SWAGGER_ENABLED:
        return False

    try:
        import drf_yasg  # noqa
    except ImportError:
        logger.info("No installation found for: drf_yasg")
        return False

    return True


class SwaggerSetup:
    @staticmethod
    def do_settings(INSTALLED_APPS):
        _show_swagger: bool = show_swagger()
        logger.info(f"Django Swagger in use: {show_swagger}")

        if not _show_swagger:
            return INSTALLED_APPS

        INSTALLED_APPS += ["drf_yasg"]

        return INSTALLED_APPS

    @staticmethod
    def do_urls(urlpatterns):
        if not show_swagger():
            return urlpatterns

        from drf_yasg import openapi
        from drf_yasg.views import get_schema_view
        from rest_framework.permissions import AllowAny
        from config.settings.swagger.schemas import GuestAPISchemeGenerator, ManagerSchemeGenerator

        guest_schema_view = get_schema_view(
            openapi.Info(
                title="Mung Manager Guest API",
                default_version="v1",
                description=(
                    "자세한 문서는 [여기](https://hiallen.notion.site/857f09c655d647dcb8eb1d8aea236e95?"
                    "v=acca72eb88a74c468d3c62cf9d751b1c&pvs=4)를 참고해주세요."
                ),
                terms_of_service="",
                contact=openapi.Contact(email="wogur981208@gmail.com"),
                license=openapi.License(name="Mung Manager Team"),
            ),
            public=True,
            generator_class=GuestAPISchemeGenerator,
            permission_classes=(AllowAny,),
        )

        manager_schema_view = get_schema_view(
            openapi.Info(
                title="Mung Manager Manager API",
                default_version="v1",
                description=(
                    "자세한 문서는 [여기](https://hiallen.notion.site/e921b91dc5784e289d9a636f53a80d05?"
                    "v=df9ebeb0a7594abf8b0341cd559371e9&pvs=4)를 참고해주세요."
                ),
                terms_of_service="",
                contact=openapi.Contact(email="wogur981208@gmail.com"),
                license=openapi.License(name="Mung Manager Team"),
            ),
            public=True,
            generator_class=ManagerSchemeGenerator,
            permission_classes=(AllowAny,),
        )

        return urlpatterns + [
            path("guest/swagger/docs", guest_schema_view.with_ui("swagger", cache_timeout=0), name="guest-schema-swagger-ui"),
            path("manager/swagger/docs", manager_schema_view.with_ui("swagger", cache_timeout=0), name="manager-schema-swagger-ui"),
        ]
