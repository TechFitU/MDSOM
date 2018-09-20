# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.admin.sites import AdminSite
import adminactions.actions as actions
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import Group
# Register your models here.
from .models import Cliente, Paciente, Dictado, Estudio, \
        Diagnostico, Doctor, Firma

User = get_user_model()

class MyAdminSite(AdminSite):
    site_header = u'MDSOM'
    site_title = u"Sistema de Diagnóstico y Radiología El Mante."
    index_title = u"Sistema de Diagnóstico y Radiología El Mante."


    def valuesQuerySetToDict(self, vqs):
        return [item for item in vqs]

    def app_index(self, request, app_label, extra_context=None):
        if extra_context is None:
            extra_context = {}
        from django.db.models import Count

        extra_context["diagnostics_count"] = Diagnostico.objects.count()
        extra_context["pacients_count"] = Paciente.objects.count()
        extra_context["studies_count"] = Estudio.objects.count()
        extra_context["sign_count"] = Firma.objects.count()
        extra_context["clients_count"] = Cliente.objects.count()
        extra_context["dictamen_count"] = Dictado.objects.count()
        extra_context["doctors_count"] = Doctor.objects.count()
        extra_context["users_count"] = User.objects.count()
        extra_context["groups_count"] = Group.objects.count()

        #Los 20 doctores con más diagnosticos
        diagnosticos_by_doctor = Doctor.objects.values('nombre').annotate(dcount=Count('diagnostico')).order_by('-dcount')[:20]
        diagnosticos_by_doctor = self.valuesQuerySetToDict(diagnosticos_by_doctor)

        diags_resultant= {}
        for elem in diagnosticos_by_doctor:
            diags_resultant[elem['nombre']]=elem['dcount']

        extra_context['diagnosticos_by_doctor'] = diags_resultant


        #Los 20 doctores con más pacientes
        pacientes_by_doctor = Doctor.objects.values('nombre').annotate(pcount=Count('pacientes')).order_by('-pcount')[:20]
        pacientes_by_doctor = self.valuesQuerySetToDict(pacientes_by_doctor)

        pacientes_por_doctor= {}
        for elem in pacientes_by_doctor:
            pacientes_por_doctor[elem['nombre']]=elem['pcount']

        extra_context['pacientes_por_doctor'] = pacientes_por_doctor


        #Los 20 pacientes con mas diagnosticos
        pacientes_con_mas_diagnosticos = Paciente.objects.values('nombre','rfc').annotate(dcount=Count('diagnostico')).order_by('-dcount')[:20]
        pacientes_con_mas_diagnosticos = self.valuesQuerySetToDict(pacientes_con_mas_diagnosticos)

        pacientes_diagnosticos= {}
        for elem in pacientes_con_mas_diagnosticos:
            pacientes_diagnosticos[elem['nombre']]=elem['dcount']

        extra_context['pacientes_diagnosticos'] = pacientes_diagnosticos


        #TODO: Las 20 fechas con más diagnosticos producidos
        diagnosticos_by_date = Diagnostico.objects.values('fecha').annotate(cantidad=Count('folio')).order_by('-cantidad')[:20]
        diagnosticos_by_date = self.valuesQuerySetToDict(diagnosticos_by_date)


        diags_by_date= {}
        for elem in diagnosticos_by_date:
            diags_by_date[elem['fecha']]=elem['cantidad']

        extra_context['diagnosticos_by_date'] = diags_by_date

        #Diagnosticos por rango de años
        diagnostico_x_anho=dict()
        anho_actual = timezone.now().year
        for i in range(int(request.POST.get('anhos',5))):
            diagnostico_x_anho[anho_actual-i] = Diagnostico.objects.filter(fecha__year = anho_actual-i).count()

        extra_context['diagnostico_x_anho'] = diagnostico_x_anho



        return super(MyAdminSite, self).app_index(request, app_label, extra_context)

    @never_cache
    def index(self, request, extra_context={}):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        from django.db.models import Count

        extra_context["diagnostics_count"] = Diagnostico.objects.count()
        extra_context["pacients_count"] = Paciente.objects.count()
        extra_context["studies_count"] = Estudio.objects.count()
        extra_context["sign_count"] = Firma.objects.count()
        extra_context["clients_count"] = Cliente.objects.count()
        extra_context["dictamen_count"] = Dictado.objects.count()
        extra_context["doctors_count"] = Doctor.objects.count()
        extra_context["users_count"] = User.objects.count()
        extra_context["groups_count"] = Group.objects.count()

        #Los 20 doctores con más diagnosticos
        diagnosticos_by_doctor = Doctor.objects.values('nombre').annotate(dcount=Count('diagnostico')).order_by('-dcount')[:20]
        diagnosticos_by_doctor = self.valuesQuerySetToDict(diagnosticos_by_doctor)

        diags_resultant= {}
        for elem in diagnosticos_by_doctor:
            diags_resultant[elem['nombre']]=elem['dcount']

        extra_context['diagnosticos_by_doctor'] = diags_resultant


        #Los 20 doctores con más pacientes
        pacientes_by_doctor = Doctor.objects.values('nombre').annotate(pcount=Count('pacientes')).order_by('-pcount')[:20]
        pacientes_by_doctor = self.valuesQuerySetToDict(pacientes_by_doctor)

        pacientes_por_doctor= {}
        for elem in pacientes_by_doctor:
            pacientes_por_doctor[elem['nombre']]=elem['pcount']

        extra_context['pacientes_por_doctor'] = pacientes_por_doctor


        #Los 20 pacientes con mas diagnosticos
        pacientes_con_mas_diagnosticos = Paciente.objects.values('nombre','rfc').annotate(dcount=Count('diagnostico')).order_by('-dcount')[:20]
        pacientes_con_mas_diagnosticos = self.valuesQuerySetToDict(pacientes_con_mas_diagnosticos)

        pacientes_diagnosticos= {}
        for elem in pacientes_con_mas_diagnosticos:
            pacientes_diagnosticos[elem['nombre']]=elem['dcount']

        extra_context['pacientes_diagnosticos'] = pacientes_diagnosticos


        #TODO: Las 20 fechas con más diagnosticos producidos
        diagnosticos_by_date = Diagnostico.objects.values('fecha').annotate(cantidad=Count('folio')).order_by('-cantidad')[:20]
        diagnosticos_by_date = self.valuesQuerySetToDict(diagnosticos_by_date)


        diags_by_date= {}
        for elem in diagnosticos_by_date:
            diags_by_date[elem['fecha']]=elem['cantidad']

        extra_context['diagnosticos_by_date'] = diags_by_date

        #Diagnosticos por rango de años
        diagnostico_x_anho=dict()
        anho_actual = timezone.now().year
        for i in range(int(request.POST.get('anhos',5))):
            diagnostico_x_anho[anho_actual-i] = Diagnostico.objects.filter(fecha__year = anho_actual-i).count()

        extra_context['diagnostico_x_anho'] = diagnostico_x_anho

        return super(MyAdminSite, self).index(request,extra_context)


admin_site = MyAdminSite(name='myadmin')
