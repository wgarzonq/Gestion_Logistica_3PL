from rest_framework import serializers
from django.utils import timezone
from rest_framework.settings import api_settings


class UsuarioSerializer(serializers.Serializer):

    TIPO_DOCUMENTO = {
        "CC": "Cédula de ciudadanía",
        "CE": "Cédula de extranjería",
        "TI": "Tarjeta de identidad",
        "PAS": "Pasaporte",
        "NIT": "Identificación Tributaria",
    }

    id = serializers.CharField(read_only=True)
    p_nombre = serializers.CharField(
        max_length=30, allow_blank=False, required=True)
    s_nombre = serializers.CharField(
        max_length=30, allow_blank=False, required=True)
    p_apellido = serializers.CharField(
        max_length=40, allow_blank=False, required=True)
    s_apellido = serializers.CharField(
        max_length=40, allow_blank=False, required=True)
    t_documento = serializers.ChoiceField(
        choices=TIPO_DOCUMENTO, allow_blank=False)
    n_documento = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    fNacimiento = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    correo = serializers.EmailField(required=True, allow_blank=False)
    n_telefono = serializers.CharField(
        max_length=16, allow_blank=False, required=True)
    en_linea = serializers.BooleanField(default=False)
    es_admin = serializers.BooleanField(default=False)
    habilitado = serializers.BooleanField(default=True)
    contra_temporal = serializers.BooleanField(default=False)
    fRegistro = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=['%d/%m/%Y %H:%M:%S'])
    contrasena = serializers.CharField(
        write_only=True, allow_blank=False, required=True)


class EmpresaSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(
        max_length=255, allow_blank=False, required=True)
    n_nit = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    correo = serializers.EmailField(required=True, allow_blank=False)
    pais = serializers.CharField(
        max_length=30, allow_blank=False, required=True)
    ciudad = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    direccion = serializers.CharField(
        max_length=60, allow_blank=False, required=True)
    n_telefono1 = serializers.CharField(
        max_length=16, allow_blank=False, required=True)
    n_telefono2 = serializers.CharField(
        max_length=16, allow_blank=True, required=False)


class VinculacionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    vinculado = serializers.BooleanField(default=False)
    es_representante = serializers.BooleanField(default=False)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    empresa = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    fecha = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=[
                                      '%d/%m/%Y %H:%M:%S'])


class ProductoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(
        max_length=30, allow_blank=False, required=True)
    categoria = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    descripcion = serializers.CharField(max_length=255, allow_blank=False, required=True, style={
                                        'base_template': 'textarea.html'})
    presentacion = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    rsanitario = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    usuario = serializers.CharField(
            max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class PedidoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    numero = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    lote = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    fCreacion = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=['%d/%m/%Y %H:%M:%S'])
    fRequerimiento = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    cantidad = serializers.IntegerField(required=True, min_value=0)
    pUnidad = serializers.FloatField(required=True, min_value=0)
    pTotal = serializers.FloatField(required=True, min_value=0)
    iva = serializers.FloatField(required=True, min_value=0)
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class ConductorSerializer(serializers.Serializer):

    TIPO_DOCUMENTO = {
        "CC": "Cédula de ciudadanía",
        "CE": "Cédula de extranjería",
        "TI": "Tarjeta de identidad",
        "PAS": "Pasaporte",
        "NIT": "Identificación Tributaria",
    }

    id = serializers.CharField(read_only=True)
    nombres = serializers.CharField(
        max_length=60, allow_blank=False, required=True)
    apellidos = serializers.CharField(
        max_length=60, allow_blank=False, required=True)
    t_documento = serializers.ChoiceField(
        choices=TIPO_DOCUMENTO, allow_blank=False)
    n_documento = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    arl = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    eps = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    telefono = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    placa = serializers.CharField(
        max_length=10, allow_blank=False, required=True)
    tVehiculo = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    usuario = serializers.CharField(
            max_length=50, allow_blank=False, required=True)


class RecepcionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    remision = serializers.CharField(max_length=20, allow_blank=False,)
    fRecogida = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hRecogida = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    vEstimado = serializers.CharField(
        max_length=4, allow_blank=False, required=True)
    fLlegada = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hLlegada = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    lote = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    fFabricacion = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    fVencimiento = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    cantidad = serializers.IntegerField(required=True, min_value=0)
    pUnidad = serializers.FloatField(required=True, min_value=0)
    pTotal = serializers.FloatField(required=True, min_value=0)
    iva = serializers.FloatField(required=True, min_value=0)
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    conductor = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class InventarioSerializer(serializers.Serializer):

    TIPO_MOVIMIENTO = {
        "ENT": "Entrada",
        "SAL": "Salida"
    }

    id = serializers.CharField(read_only=True)
    fecha = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=[
                                      '%d/%m/%Y %H:%M:%S'])
    tMovimiento = serializers.ChoiceField(
        choices=TIPO_MOVIMIENTO, allow_blank=False)
    cantidad = serializers.IntegerField(required=True, min_value=0)
    stock = serializers.IntegerField(required=True, min_value=0)
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    recepcion = serializers.CharField(
        max_length=50, allow_blank=True, required=False)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class DockingSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    numero = serializers.CharField(
        max_length=11, allow_blank=False, required=True)
    fInicio = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hInicio = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    fFin = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hFin = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    tEstancia = serializers.IntegerField(required=True, min_value=0)
    estado = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    aAsignada = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    pedido = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class AlistamientoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    numero = serializers.CharField(
        max_length=11, allow_blank=False, required=True)
    tipo = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    lote = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    fInicio = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hInicio = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    fFin = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hFin = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    estado = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    aAsignada = serializers.CharField(
        max_length=15, allow_blank=False, required=True)
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    pedido = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)


class DespachoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    remision = serializers.CharField(
        max_length=11, allow_blank=False, required=True)
    fRecogida = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hRecogida = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    vEstimado = serializers.CharField(
        max_length=4, allow_blank=False, required=True)
    fLlegada = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    hLlegada = serializers.TimeField(
        format=api_settings.TIME_FORMAT, input_formats=['%H:%M:%S'])
    lote = serializers.CharField(
        max_length=20, allow_blank=False, required=True)
    fFabricacion = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    fVencimiento = serializers.DateField(
        format=api_settings.DATE_FORMAT, input_formats=['%d/%m/%Y'])
    producto = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    conductor = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    pedido = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    usuario = serializers.CharField(
        max_length=50, allow_blank=False, required=True)
    data = serializers.JSONField(default=dict, required=False)
