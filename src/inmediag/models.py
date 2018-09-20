# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords


User = settings.AUTH_USER_MODEL

# Create your models here.
class Estado(models.Model):    
    idestado = models.CharField(primary_key=True, max_length=25)    
    nombre = models.CharField(max_length=45)
    

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        #db_table = "estado"             
        verbose_name="estado"
        verbose_name_plural="estados"

class Municipio(models.Model):
    idmunicipio = models.IntegerField(primary_key=True)    
    idestado = models.ForeignKey(Estado, db_column="idestado", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % self.nombre

    class Meta:
        #db_table = "municipio"             
        verbose_name="municipio"
        verbose_name_plural="municipios"

class Paciente(models.Model):
    nombre = models.CharField(max_length=150)
    rfc = models.CharField(verbose_name="ID", max_length=30, blank=True, null=True, default="Desconocido")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)
    history = HistoricalRecords()

    def complete_name(self):
        return u"%s" % (self.nombre,)

    complete_name.short_description = "Nombre completo"
    complete_name.admin_order_field = "nombre"

    def __unicode__(self):
        return u"%s. RFC: %s" % (self.nombre, self.rfc)

    class Meta:
        #db_table = "Paciente"
        ordering = ['-creado']
        get_latest_by = 'creado'        
        verbose_name="paciente"
        verbose_name_plural="pacientes"

class Cliente(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    rfc = models.CharField(verbose_name="RFC", max_length=30, unique=True, null=True, blank=True)
    domicilio = models.TextField()
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)
    municipio = ChainedForeignKey(
        Municipio, 
        chained_field="estado",
        chained_model_field="idestado", 
        show_all=False, 
        auto_choose=True
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)
    history = HistoricalRecords()

    def complete_name(self):
        return u"%s" % (self.nombre,)

    complete_name.short_description = "Nombre completo"
    complete_name.admin_order_field = "nombre"

    def __str__(self):
        return u"%s. RFC: %s" % (self.nombre, self.rfc)

    class Meta:
        #db_table = "Paciente"
        ordering = ['-creado']
        get_latest_by = 'creado'        
        verbose_name="cliente"
        verbose_name_plural="clientes"

class Estudio(models.Model):
    descripcion = models.CharField("Descripción", max_length=75)
    costo = models.DecimalField(max_digits=6, decimal_places=2)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)

    def __str__(self):
        return u"%s" %(self.descripcion,)

    class Meta:
        #db_table = "Paciente"
        ordering = ['descripcion']
        get_latest_by = 'creado'        
        verbose_name="estudio"
        verbose_name_plural="estudios"

class Dictado(models.Model):
    texto = models.TextField("Texto", null=True, blank=True)
    estudio = models.ForeignKey(Estudio, on_delete=models.SET_NULL, null=True)
    creado_por = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return u"Dictado del estudio " + str(self.estudio)
    class Meta:
        #db_table = "Paciente"
        ordering = ['-creado']
        get_latest_by = 'creado'        
        verbose_name="dictado"
        verbose_name_plural="dictados"
        
class Firma(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    firma = models.CharField(max_length=50)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)
    
    def __str__(self):
        return u"%s" %(self.firma)

    class Meta:
        #db_table = "Paciente"
        ordering = ['-creado']
        get_latest_by = 'creado'        
        verbose_name="firma"
        verbose_name_plural="Firmas"

class Doctor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    domicilio = models.TextField(max_length=150, null=True, blank=True)
    celular = models.CharField(max_length=50, null=True, blank=True)
    telefono_particular = models.CharField(max_length=50, null=True, blank=True)
    pacientes = models.ManyToManyField(Paciente, db_table="inmediag_doctor_paciente", \
                                    verbose_name="Pacientes", blank=True, editable=False)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)

    def __str__(self):
        return u"%s" %(self.nombre,)

    def diagnosticos(self):
        return self.diagnostico_set.count()

    diagnosticos.short_description = u"Diagnósticos"

    def numero_pacientes(self):
        return self.pacientes.count();
    numero_pacientes.short_description = u"Pacientes"
           
    def __unicode__(self):
        return u"%s" %(self.nombre,)
    class Meta:
        #db_table = "Paciente"
        ordering = ['-creado']
        get_latest_by = 'creado'        
        verbose_name="doctor"
        verbose_name_plural="doctores"

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
def folio_generator():
    import random
    import string
    folio = "".join([random.SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation) for i in
                   range(50)]).replace("&", "*")
    return folio

from django.utils.html import format_html
class Diagnostico(models.Model):
    folio = models.CharField("Folio", default=folio_generator,primary_key=True, max_length=50)
    pendiente = models.BooleanField('Pendiente',editable=True,default=True)
    fecha = models.DateTimeField(default= timezone.now)
    diagnostico = models.TextField(u"Diagnóstico",null=True, blank=True)
    
    #foto1 = FilerImageField(null=True, blank=True, related_name="diagnostico_1")

    estudio = models.ForeignKey(Estudio, on_delete=models.SET_NULL, null=True)
    dictado = ChainedForeignKey(
        Dictado, 
        chained_field="estudio",
        chained_model_field="estudio", 
        show_all=False,
        auto_choose=True,
        null=True,
    )

    paciente=models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    firma = models.ForeignKey(Firma, null=True, on_delete=models.SET_NULL)
    
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return u"Diagnostico con folio %s, fecha %s, costo %s" %(self.folio, self.fecha, self.estudio.costo)

    def diagnostic_status(self):
        if self.pendiente:
            return format_html('<div style="width:100%%; height:100%%; background-color:orange;">{}</div>', 'Pendiente')
        return format_html('<div style="width:100%%; height:100%%; background-color:green;">{}</div>', 'Completado') 
    
    diagnostic_status.short_description="Estado"


    class Meta:
        #db_table = "Paciente"
        ordering = ['-folio']
        get_latest_by = 'folio'        
        verbose_name=u"diagnóstico"
        verbose_name_plural=u"diagnósticos"



# from ajax_upload.models import UploadedImage
# from django.utils.translation import ugettext_lazy as _
# class Imagen (UploadedImage):
#     diagnostico = models.ForeignKey(Diagnostico, related_name="images")

#     class Meta:
#         ordering = ('id',)

#         verbose_name = u'Imagen'
#         verbose_name_plural = u'Imágenes'
#         db_table = "inmediag_imagen"