# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.forms.models import BaseInlineFormSet
from simple_history.admin import SimpleHistoryAdmin

from ajax_select.admin import AjaxSelectAdmin
from liststyle.admin import ListStyleAdminMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import DiagnosticoForm

# Resources and ImportExportModelAdmin of import-export app
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields

# from inmediag.forms import ImagenForm
# Register your models here.
from .models import Cliente, Paciente, Dictado, Estudio, \
    Diagnostico, Doctor, Firma, Estado, Municipio


class PacienteAdmin(SimpleHistoryAdmin):
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = ('nombre', 'rfc', 'creado', 'ultima_actualizacion')

    # Results per page
    list_per_page = 30

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['nombre', 'rfc', 'doctor__nombre']
    list_filter = ['creado', 'doctor']
    readonly_fields = ('creado_por',)

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user

        obj.save()


class DoctorAdmin(admin.ModelAdmin):
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = ('nombre', 'celular', 'diagnosticos', 'numero_pacientes', 'creado', 'ultima_actualizacion')

    # Results per page
    list_per_page = 30

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['nombre', 'celular', 'telefono_particular', 'domicilio']
    list_filter = ['creado', ]
    readonly_fields = ('creado_por',)

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user

        obj.save()


class ClienteAdmin(SimpleHistoryAdmin):
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = ('nombre', 'rfc', 'estado', 'municipio', 'creado', 'ultima_actualizacion')

    # Results per page
    list_per_page = 30

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['nombre', 'rfc']
    list_filter = ['creado', 'municipio', 'estado']
    readonly_fields = ('creado_por',)

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user

        obj.save()


class DictadoInlineFormSet(BaseInlineFormSet):

    def save(self, **kwargs):
        super(DictadoInlineFormSet, self).save(commit=False)

        # Colocando a cada nueva instancia de Dictado que maneja este InlineFormSet,
        # el usuario que lo registra
        for instance in self.new_objects:
            instance.creado_por = instance.estudio.creado_por
            instance.save()

        super(DictadoInlineFormSet, self).save()


class DictadoInline(admin.StackedInline):
    model = Dictado
    # form = VehiculoForm
    formset = DictadoInlineFormSet
    # fields = (
    #     ('serie', 'marca', 'modelo', 'anho_modelo',),
    #     ('placa', 'tarjeta_circulacion','tipo',  'creado_por',),
    #     ('capacidad_lt', 'capacidad_kg', 'capacidad_personas'),

    # )
    readonly_fields = ('creado_por',)
    extra = 1


class EstudioAdmin(admin.ModelAdmin):
    """
    Customize the look of the auto-generated admin for the Estudio model
    1. Changing the way in each choice in database is shown
    (new one is in table form, with more than a column)
    2. Displaying the way of adding new question objects,
    including adding new choices inline(TabularInline in this case).
    3. Filtering in "change list" page of Persona, using list_filter
    3. Inserting fieldsets in question forms, with all fields by fieldset
    """
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = ('descripcion', 'costo', 'creado', 'ultima_actualizacion')

    # Results per page
    list_per_page = 30

    inlines = [DictadoInline, ]

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['descripcion', ]

    readonly_fields = ('creado_por',)

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user

        obj.save()


class DictadoAdmin(SimpleHistoryAdmin):
    """
    Customize the look of the auto-generated admin for the Dictado model
    1. Changing the way in each choice in database is shown
    (new one is in table form, with more than a column)
    2. Displaying the way of adding new question objects,
    including adding new choices inline(TabularInline in this case).
    3. Filtering in "change list" page of Persona, using list_filter
    3. Inserting fieldsets in question forms, with all fields by fieldset
    """
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = ('texto', 'estudio', 'creado', 'ultima_actualizacion')

    # Results per page
    list_per_page = 30

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['texto', 'estudio__nombre', ]

    readonly_fields = ('creado_por',)

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user

        obj.save()


# Define an inline admin descriptor for Imagen model
# class ImageInline(admin.TabularInline):
#     model = Imagen
#     form = ImagenForm
#     verbose_name_plural = u'Imágenes médicas'
#     extra = 1
#     max_num=5

class DiagnosticoResource(resources.ModelResource):
    # Personalizando un campo en la importacion o exportacion, aqui se muestra la informacion
    # personalizada del vehiculo

    # vehiculo_completo = fields.Field()
    # def dehydrate_vehiculo_completo(self, obj):
    #    return 'Placa %s, marca %s, modelo %s' % (obj.vehiculo.placa, obj.vehiculo.marca, obj.vehiculo.modelo)

    # Redefinicion del nombre de la columna para cada campo en la exportacion

    folio = fields.Field(attribute="folio", column_name=u'FOLIO CONSULTA')
    pendiente = fields.Field(attribute="pendiente", column_name=u'ESTADO')
    paciente = fields.Field(attribute="paciente", column_name=u'NOMBRE DEL PACIENTE')
    estudio = fields.Field(attribute="estudio", column_name=u'ESTUDIO REALIZADO')
    dictado = fields.Field(attribute="dictado", column_name=u'DICTADO REFERENCIA')
    diagnostico = fields.Field(attribute="diagnostico", column_name=u'DIAGNÓSTICO')
    fecha = fields.Field(attribute="fecha", column_name=u'FECHA CONSULTA')
    doctor = fields.Field(attribute="doctor", column_name=u'DOCTOR REMITIÓ')
    firma = fields.Field(attribute="firma", column_name=u'RADIÓLOGO')
    creado = fields.Field(attribute="creado", column_name=u'FECHA CREACIÓN')
    ultima_actualizacion = fields.Field(attribute="ultima_actualizacion", column_name=u'ÚLTIMA ACTUALIZACIÓN')

    class Meta:
        model = Diagnostico
        fields = ('folio', 'pendiente', 'paciente', 'estudio', \
                  'dictado', 'diagnostico', 'fecha', \
                  'doctor', 'firma', 'creado', 'ultima_actualizacion')
        export_order = ('folio', 'pendiente', 'paciente', 'estudio', \
                        'dictado', 'diagnostico', 'fecha', \
                        'doctor', 'firma', 'creado', 'ultima_actualizacion')

        widgets = {

            'fecha': {'format': '%d/%m/%Y'},
        }
        skip_unchanged = True  # Saltar los registros importados que no tienen cambios respecto a tabla
        report_skipped = True  # True haria que se no muestren los registros sin cambios que se importan


from django.utils.html import format_html
from .views import render_to_pdf
from django.shortcuts import get_object_or_404


class DiagnosticoAdmin(AjaxSelectAdmin, ListStyleAdminMixin, ImportExportModelAdmin):
    """
    Customize the look of the auto-generated admin for the Diagnostico model
    1. Changing the way in each choice in database is shown
    (new one is in table form, with more than a column)
    2. Displaying the way of adding new question objects,
    including adding new choices inline(TabularInline in this case).
    3. Filtering in "change list" page of Persona, using list_filter
    3. Inserting fieldsets in question forms, with all fields by fieldset
    """

    resource_class = DiagnosticoResource
    # Displaying each row in "change list" page, if list_display is not provided,
    # Django will use str() method to display each question,
    # that use our __unicode__() implementation

    list_display = (
    'folio', 'diagnostic_status', 'print_diagnostic', 'estudio', 'doctor', 'firma', 'fecha', 'ultima_actualizacion')

    # Fields in form
    def get_fields(self, request, obj=None):
        if not request.user.is_superuser:
            try:
                # Si el usario logueado es doctor que firma el diagnostico si puede ver todos los campos del diagnostico
                if request.user.groups.filter(name="DOCTORES").exists():
                    return (
                        ('folio', 'paciente', 'doctor', 'fecha',),
                        ('estudio', 'dictado', 'diagnostico'),
                        ('pendiente', 'firma', 'creado_por')
                    )
                if request.user.groups.filter(name="RECEPCIONISTAS").exists():
                    return (
                        ('paciente', 'doctor', 'fecha'),
                        ('folio', 'estudio', 'creado_por')
                    )

            except ObjectDoesNotExist:
                pass

        return (
            ('folio', 'paciente', 'doctor', 'fecha',),
            ('estudio', 'dictado', 'diagnostico'),
            ('pendiente', 'firma', 'creado_por')
        )

    # Results per page
    list_per_page = 30

    def print_diagnostic(self, obj):
        return format_html(
            '<a class="btn btn-info" target="_blank" href="/admin/inmediag/diagnostico/imprimir/{}/" title="Imprimir diagn&oacute;stico"><span class="glyphicon glyphicon-print"></span></a>',
            obj.folio)

    print_diagnostic.short_description = "Imprimir"

    def print_diagnostic_view(self, request, diagnostico):
        # ...
        try:
            diagObject = get_object_or_404(Diagnostico, pk=diagnostico)
            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                # Anything else you want in the context...
                diagnostico=diagObject,
                pagesize="Letter"
            )

        except ObjectDoesNotExist:
            context = dict()

        return render_to_pdf('admin/inmediag/sometemplate.html', context)

    def get_urls(self):
        from django.conf.urls import url
        urls = super(DiagnosticoAdmin, self).get_urls()
        my_urls = [
            url(r'^imprimir/(?P<diagnostico>[0-9]+)/$', self.admin_site.admin_view(self.print_diagnostic_view),
                name="dsd"),
        ]
        return my_urls + urls

    def get_row_css(self, obj, index):
        if obj.pendiente:
            return 'danger red%d' % index
        return ''

    # Creando una nueva acción en la administracion, que convierte diagnosticos seleccionados de pendientes a completados
    def make_completed_diagnostics(self, request, queryset):
        rows_updated = queryset.update(pendiente=False)
        if rows_updated == 1:
            message_bit = u"1 diagnóstico fue "
        else:
            message_bit = u"%s diagnósticos fueron " % rows_updated
        self.message_user(request, "%s correctamente actualizado(s)." % message_bit)

    make_completed_diagnostics.short_description = u"Confirmar diagnósticos completados"
    make_completed_diagnostics.name = "make_completed_diagnostics"

    # Creando una nueva acción en la administracion, que convierte diagnosticos seleccionados en pendientes
    def make_uncompleted_diagnostics(self, request, queryset):
        rows_updated = queryset.update(pendiente=True)
        if rows_updated == 1:
            message_bit = u"1 diagnóstico fue"
        else:
            message_bit = u"%s diagnósticos fueron " % rows_updated
        self.message_user(request, "%s correctamente actualizado(s)." % message_bit)

    make_uncompleted_diagnostics.short_description = u"Marcar diagnósticos como pendientes"
    make_uncompleted_diagnostics.name = "make_uncompleted_diagnostics"

    actions = ['make_uncompleted_diagnostics', 'make_completed_diagnostics']

    # Activando las acciones por condicionales
    # Solo para los medicos se habilita la opcion de marcar diagnosticos como completados
    def get_actions(self, request):
        action_dict = super(DiagnosticoAdmin, self).get_actions(request)

        if not request.user.is_superuser and not request.user.groups.filter(name="DOCTORES").exists():

            if 'make_uncompleted_diagnostics' in action_dict:
                del action_dict['make_uncompleted_diagnostics']
            if 'make_completed_diagnostics' in action_dict:
                del action_dict['make_completed_diagnostics']

        return action_dict

    def get_queryset(self, request):
        """
        Este metodo permite distinguir los objetos que pueden ser vistos en la "change list", o editados de acuerdo
        a condiciones especificas.
        En este caso permitimos que el superusuario vea todo, pero si es un doctor (y es el que firma) el usuario logueado
        solo vea los diagnosticos asignados.
        mismo. Los usuarios RECEPCIONISTAS, o sea, los que registran los diagnosticos pueden ver todo.
        El resto de los usuarios no puede ver nada.
        """
        qs = super(DiagnosticoAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            try:
                # Si el usario logueado es doctor que firma el diagnostico si puede ver los diagnosticos de él
                firma_obj = Firma.objects.get(usuario=request.user)
                if request.user.groups.filter(name="DOCTORES").exists():
                    qs = qs.filter(firma=firma_obj)
                elif request.user.groups.filter(name="RECEPCIONISTAS").exists():
                    pass
                else:
                    qs = []


            except ObjectDoesNotExist:

                pass

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "firma" and request.user.groups.filter(name="DOCTORES").exists():
            kwargs["queryset"] = Firma.objects.filter(usuario=request.user)
        return super(DiagnosticoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Adding some search capabilities, searching in all text fields.
    search_fields = ['folio', 'estudio__descripcion', ]

    list_filter = ['fecha', 'pendiente', 'doctor', ]
    readonly_fields = ('creado_por', 'folio')
    # inlines = (ImageInline,)

    form = DiagnosticoForm

    def save_model(self, request, obj, form, change):
        # Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        # tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user
        # Se salva el diagnostico
        obj.save()

        # Se guardan el paciente y el doctor involucrados en el diagnostico
        paciente = obj.paciente
        doctor = obj.doctor

        # Se salva al paciente en el conjunto de pacientes de ese doctor
        doctor.pacientes.add(paciente)


# Define an inline admin descriptor for ResponsableMaterial model
# which acts a bit like a singleton
class FirmaInline(admin.StackedInline):
    model = Firma
    can_delete = False
    verbose_name = 'Datos del doctor'
    verbose_name_plural = 'Doctor Firmante'
    max_num = 1


# Define a new User admin
class MyUserAdmin(UserAdmin):
    inlines = (FirmaInline,)


# Import my custom subclass of AdminSite
from .myadmin import admin_site
# Add the actions to your site
import adminactions.actions as actions

# register selected adminactions in my site
admin_site.add_action(actions.mass_update)
admin_site.add_action(actions.export_as_csv)
admin_site.add_action(actions.export_as_xls)
admin_site.add_action(actions.graph_queryset)

#### REGISTERING MODELS WITH THEIR CORRESPONDING MODEL ADMIN####
#admin.site.unregister(User)
admin_site.register(Paciente, PacienteAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(User, MyUserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Firma)
admin_site.register(Doctor, DoctorAdmin)
admin_site.register(Estudio, EstudioAdmin)
admin_site.register(Dictado, DictadoAdmin)
admin_site.register(Diagnostico, DiagnosticoAdmin)
