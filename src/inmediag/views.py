from html import escape

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

from .models import Dictado


# Create your views here.
@login_required
def get_dictado_by_id(request, identificador):
    import json
    try:
        dictado = get_object_or_404(Dictado, pk=identificador)
        data = json.dumps(dictado.texto)
    except ObjectDoesNotExist:
        data = json.dumps(None)
    return HttpResponse(data, content_type="application/json")


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


# Custom Http handlers
def my_custom_permission_denied_view(request):
    context = {}
    return render(request, "admin/inmediag/403.html", context)


def my_custom_page_not_found_view(request):
    context = {}
    return render(request, "admin/inmediag/404.html", context)


def my_custom_error_view(request):
    context = {}
    return render(request, "admin/inmediag/500.html", context)
