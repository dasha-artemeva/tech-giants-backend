from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

UI_TAGS = ['SSR']


@extend_schema(
    tags=UI_TAGS,
)
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([])
def index(request: Request) -> Response:
    return Response(
        template_name='index.html',
    )


@extend_schema(
    tags=UI_TAGS,
)
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([])
def lk(request: Request) -> Response:
    if request.user.is_anonymous:
        return redirect(reverse('ui:index'))
    return Response(
        template_name='lk.html',
    )
