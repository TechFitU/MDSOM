from ajax_select import LookupChannel, register
from django.utils.html import escape
from django.db.models import Q
from inmediag.models import Paciente, Doctor

@register('pacientes')
class PacienteLookup(LookupChannel):

    model = Paciente

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(nombre__icontains=q) | Q(rfc__icontains=q)
            ).order_by('nombre')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s - %s" % (escape(obj.nombre),obj.rfc)

@register('doctores')
class DoctorLookup(LookupChannel):

    model = Doctor

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(nombre__icontains=q) | Q(celular__icontains=q) | Q(telefono_particular__icontains=q)
            ).order_by('nombre')

    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return str(obj)

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(obj.nombre))