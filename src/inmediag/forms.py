from django import forms
#from ajax_upload.widgets import AjaxClearableImageFileInput
#from ajax_upload.forms import UploadedImageForm
from inmediag.models import  Paciente, Diagnostico
from django.forms import ModelForm

#from inmediag.models import Imagen

#Import make_ajax_field helper to build an ajax form field 
from ajax_select import make_ajax_field


# class ImagenForm(UploadedImageForm):
#     class Meta:
#         model = Imagen
#         fields = ("file",)
#         localized_fields = "__all__"
#         widgets = {
#             'file': AjaxClearableImageFileInput
#         }


class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = "__all__"
        localized_fields = "__all__"

        # widgets ={
        #     'nombre': ClearableInput(),
        #     'apellidos': ClearableInput(),
        #     'rfc': ClearableInput(),

        # }
    
    paciente  = make_ajax_field(Meta.model, 'paciente', 'pacientes',
        help_text="Buscar nombre, apellidos, rfc del paciente", show_help_text=True, required=True,
        plugin_options = {'autoFocus': True, 'minLength': 4})

    doctor  = make_ajax_field(Diagnostico, 'doctor', 'doctores',
        help_text="Buscar nombre, apellidos, telefono del doctor", show_help_text=True, required=True,
        plugin_options = {'autoFocus': True, 'minLength': 4})