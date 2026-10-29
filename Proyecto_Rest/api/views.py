from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from datetime import datetime, date, time
from .conversion import convertir_documento

# --------------------------- Usuario --------------------------


@permission_classes((permissions.AllowAny,))
class UsuarioListCreateView(APIView):

    def get(self, request):
        usuarios = [
            convertir_documento(usuario)
            for usuario in usuario_collection.find()
        ]

        serializer = UsuarioSerializer(usuarios, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = UsuarioSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        usuarios = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(usuario):
            usuario = dict(usuario)

            if isinstance(usuario.get("fNacimiento"), date):
                usuario["fNacimiento"] = datetime.combine(
                    usuario["fNacimiento"],
                    time.min
                )

            return usuario

        # Registrar varios usuarios
        if es_lista:
            if not usuarios:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            usuarios = [
                convertir_fechas(usuario)
                for usuario in usuarios
            ]

            result = usuario_collection.insert_many(usuarios)

            respuesta = []

            for usuario, object_id in zip(usuarios, result.inserted_ids):
                usuario["_id"] = object_id
                respuesta.append(convertir_documento(usuario))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo usuario
        usuario = convertir_fechas(usuarios)
        result = usuario_collection.insert_one(usuario)

        usuario["_id"] = result.inserted_id

        usuario = convertir_documento(usuario)

        return Response(
            usuario,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(usuario):
            usuario = dict(usuario)

            if isinstance(usuario.get("fNacimiento"), date):
                usuario["fNacimiento"] = datetime.combine(
                    usuario["fNacimiento"],
                    time.min
                )

            return usuario

        # Caso 1: actualizar varios usuarios
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del usuario"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = UsuarioSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                usuario_data = convertir_fechas(
                    serializer.validated_data
                )

                result = usuario_collection.update_one(
                    {"_id": object_id},
                    {"$set": usuario_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Usuario no encontrado"
                    })
                    continue

                usuario = usuario_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(usuario))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class UsuarioDetailView(APIView):

    def get(self, request, usuario_id):

        try:
            object_id = ObjectId(usuario_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = usuario_collection.find_one({
            "_id": object_id
        })

        if not usuario:
            return Response(
                {"error": "Usuario no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        usuario = convertir_documento(usuario)

        serializer = UsuarioSerializer(usuario)

        return Response(serializer.data)

    def put(self, request, usuario_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(usuario):
            usuario = dict(usuario)

            if isinstance(usuario.get("fNacimiento"), date):
                usuario["fNacimiento"] = datetime.combine(
                    usuario["fNacimiento"],
                    time.min
                )

            return usuario

        # Caso 2: actualizar un solo usuario
        if not usuario_id:
            return Response(
                {"error": "Debes proporcionar el ID del usuario"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(usuario_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UsuarioSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        usuario_data = convertir_fechas(
            serializer.validated_data
        )

        result = usuario_collection.update_one(
            {"_id": object_id},
            {"$set": usuario_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        usuario = usuario_collection.find_one(
            {"_id": object_id}
        )

        usuario = convertir_documento(usuario)

        return Response(usuario, status=status.HTTP_200_OK)

    def delete(self, request, usuario_id):

        try:
            object_id = ObjectId(usuario_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = usuario_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Usuario no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Empresa ------------------


@permission_classes((permissions.AllowAny,))
class EmpresaListCreateView(APIView):

    def get(self, request):
        empresas = [
            convertir_documento(empresa)
            for empresa in empresa_collection.find()
        ]

        serializer = EmpresaSerializer(empresas, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = EmpresaSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        empresas = serializer.validated_data

        # Registrar varias empresas
        if es_lista:
            if not empresas:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = empresa_collection.insert_many(empresas)

            respuesta = []

            for empresa, object_id in zip(empresas, result.inserted_ids):
                empresa["_id"] = object_id
                respuesta.append(convertir_documento(empresa))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar una sola empresa
        empresa = dict(empresas)
        result = empresa_collection.insert_one(empresa)

        empresa["_id"] = result.inserted_id

        empresa = convertir_documento(empresa)

        return Response(
            empresa,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Caso 1: actualizar varias empresas
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID de la empresa"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = EmpresaSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                result = empresa_collection.update_one(
                    {"_id": object_id},
                    {"$set": serializer.validated_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Empresa no encontrada"
                    })
                    continue

                empresa = empresa_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(empresa))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class EmpresaDetailView(APIView):

    def get(self, request, empresa_id):

        try:
            object_id = ObjectId(empresa_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        empresa = empresa_collection.find_one({
            "_id": object_id
        })

        if not empresa:
            return Response(
                {"error": "Empresa no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        empresa = convertir_documento(empresa)

        serializer = EmpresaSerializer(empresa)

        return Response(serializer.data)

    def put(self, request, empresa_id=None):
        data = request.data

        # Caso 2: actualizar una sola empresa
        if not empresa_id:
            return Response(
                {"error": "Debes proporcionar el ID de la empresa"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(empresa_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EmpresaSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        result = empresa_collection.update_one(
            {"_id": object_id},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Empresa no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        empresa = empresa_collection.find_one(
            {"_id": object_id}
        )

        empresa = convertir_documento(empresa)

        return Response(empresa, status=status.HTTP_200_OK)

    def delete(self, request, empresa_id):

        try:
            object_id = ObjectId(empresa_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = empresa_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Empresa no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Vinculación ------------------


@permission_classes((permissions.AllowAny,))
class VinculacionListCreateView(APIView):

    def get(self, request):

        vinculaciones = []

        for documento in vinculacion_collection.find():
            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Buscar la empresa relacionada
            empresa_id = documento.get("empresa")

            empresa = empresa_collection.find_one({
                "_id": ObjectId(empresa_id)
            }) if empresa_id else None

            print(empresa)

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir la empresa
            if empresa:
                empresa = convertir_documento(empresa)
                empresa = EmpresaSerializer(empresa).data

            # Convertir la vinculación
            vinculacion = convertir_documento(documento)

            # Agregar los datos relacionados
            vinculacion["usuario"] = usuario
            vinculacion["empresa"] = empresa

            vinculaciones.append(vinculacion)

        serializer = VinculacionSerializer(vinculaciones, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = VinculacionSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        vinculaciones = serializer.validated_data

        # Registrar varias vinculaciones
        if es_lista:
            if not vinculaciones:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = vinculacion_collection.insert_many(vinculaciones)

            respuesta = []

            for vinculacion, object_id in zip(vinculaciones, result.inserted_ids):
                vinculacion["_id"] = object_id
                respuesta.append(convertir_documento(vinculacion))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar una sola vinculación
        vinculacion = dict(vinculaciones)
        result = vinculacion_collection.insert_one(vinculacion)

        vinculacion["_id"] = result.inserted_id

        vinculacion = convertir_documento(vinculacion)

        return Response(
            vinculacion,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Caso 1: actualizar varias vinculaciones
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID de la vinculación"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = VinculacionSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                result = vinculacion_collection.update_one(
                    {"_id": object_id},
                    {"$set": serializer.validated_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Vinculación no encontrada"
                    })
                    continue

                vinculacion = vinculacion_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(vinculacion))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class VinculacionDetailView(APIView):

    def get(self, request, vinculacion_id):

        try:
            object_id = ObjectId(vinculacion_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar la vinculación
        documento = vinculacion_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Vinculación no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Buscar la empresa relacionada
        empresa_id = documento.get("empresa")

        empresa = empresa_collection.find_one({
            "_id": ObjectId(empresa_id)
        }) if empresa_id else None

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir la empresa
        if empresa:
            empresa = convertir_documento(empresa)
            empresa = EmpresaSerializer(empresa).data

        # Convertir la vinculación
        vinculacion = convertir_documento(documento)

        # Reemplazar los IDs por los objetos relacionados
        vinculacion["usuario"] = usuario
        vinculacion["empresa"] = empresa

        serializer = VinculacionSerializer(vinculacion)

        return Response(serializer.data)

    def put(self, request, vinculacion_id=None):
        data = request.data

        # Caso 2: actualizar una sola vinculación
        if not vinculacion_id:
            return Response(
                {"error": "Debes proporcionar el ID de la vinculación"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(vinculacion_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VinculacionSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        result = vinculacion_collection.update_one(
            {"_id": object_id},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Vinculación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        vinculacion = vinculacion_collection.find_one(
            {"_id": object_id}
        )

        vinculacion = convertir_documento(vinculacion)

        return Response(vinculacion, status=status.HTTP_200_OK)

    def delete(self, request, vinculacion_id):

        try:
            object_id = ObjectId(vinculacion_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = vinculacion_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Vinculación no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Producto ------------------


@permission_classes((permissions.AllowAny,))
class ProductoListCreateView(APIView):

    def get(self, request):
        productos = []

        for documento in producto_collection.find():

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el producto
            producto = convertir_documento(documento)

            # Agregar los datos relacionados
            producto["usuario"] = usuario

            productos.append(producto)

        serializer = ProductoSerializer(productos, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = ProductoSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        productos = serializer.validated_data

        # Registrar varios productos
        if es_lista:
            if not productos:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = producto_collection.insert_many(productos)

            respuesta = []

            for producto, object_id in zip(productos, result.inserted_ids):
                producto["_id"] = object_id
                respuesta.append(convertir_documento(producto))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo producto
        producto = dict(productos)
        result = producto_collection.insert_one(producto)

        producto["_id"] = result.inserted_id

        producto = convertir_documento(producto)

        return Response(
            producto,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Caso 1: actualizar varios productos
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del producto"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = ProductoSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                result = producto_collection.update_one(
                    {"_id": object_id},
                    {"$set": serializer.validated_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Producto no encontrado"
                    })
                    continue

                producto = producto_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(producto))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class ProductoDetailView(APIView):

    def get(self, request, producto_id):

        try:
            object_id = ObjectId(producto_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el producto
        documento = producto_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Producto no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")
        
        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el producto
        producto = convertir_documento(documento)

        # Agregar los datos relacionados
        producto["usuario"] = usuario

        serializer = ProductoSerializer(producto)

        return Response(serializer.data)

    def put(self, request, producto_id=None):
        data = request.data

        # Caso 2: actualizar un solo producto
        if not producto_id:
            return Response(
                {"error": "Debes proporcionar el ID del producto"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(producto_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductoSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        result = producto_collection.update_one(
            {"_id": object_id},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        producto = producto_collection.find_one(
            {"_id": object_id}
        )

        producto = convertir_documento(producto)

        return Response(producto, status=status.HTTP_200_OK)

    def delete(self, request, producto_id):

        try:
            object_id = ObjectId(producto_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = producto_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Producto no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Pedido ------------------


@permission_classes((permissions.AllowAny,))
class PedidoListCreateView(APIView):

    def get(self, request):
        pedidos = []

        for documento in pedido_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el pedido
            pedido = convertir_documento(documento)

            # Agregar los datos relacionados
            pedido["producto"] = producto
            pedido["usuario"] = usuario

            pedidos.append(pedido)

        serializer = PedidoSerializer(pedidos, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = PedidoSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        pedidos = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(pedido):
            pedido = dict(pedido)

            if isinstance(pedido.get("fRequerimiento"), date):
                pedido["fRequerimiento"] = datetime.combine(
                    pedido["fRequerimiento"],
                    time.min
                )

            return pedido

        # Registrar varios pedidos
        if es_lista:
            if not pedidos:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            pedidos = [
                convertir_fechas(pedido)
                for pedido in pedidos
            ]

            result = pedido_collection.insert_many(pedidos)

            respuesta = []

            for pedido, object_id in zip(pedidos, result.inserted_ids):
                pedido["_id"] = object_id
                respuesta.append(convertir_documento(pedido))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo pedido
        pedido = convertir_fechas(pedidos)
        result = pedido_collection.insert_one(pedido)

        pedido["_id"] = result.inserted_id

        pedido = convertir_documento(pedido)

        return Response(
            pedido,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(pedido):
            pedido = dict(pedido)

            if isinstance(pedido.get("fRequerimiento"), date):
                pedido["fRequerimiento"] = datetime.combine(
                    pedido["fRequerimiento"],
                    time.min
                )

            return pedido

        # Caso 1: actualizar varios pedidos
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del pedido"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = PedidoSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                pedido_data = convertir_fechas(
                    serializer.validated_data
                )

                result = pedido_collection.update_one(
                    {"_id": object_id},
                    {"$set": pedido_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Pedido no encontrado"
                    })
                    continue

                pedido = pedido_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(pedido))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class PedidoDetailView(APIView):

    def get(self, request, pedido_id):

        try:
            object_id = ObjectId(pedido_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el pedido
        documento = pedido_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Pedido no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el pedido
        pedido = convertir_documento(documento)

        # Agregar los datos relacionados
        pedido["producto"] = producto
        pedido["usuario"] = usuario

        # Serializar la respuesta
        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)

    def put(self, request, pedido_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(pedido):
            pedido = dict(pedido)

            if isinstance(pedido.get("fRequerimiento"), date):
                pedido["fRequerimiento"] = datetime.combine(
                    pedido["fRequerimiento"],
                    time.min
                )

            return pedido

        # Caso 2: actualizar un solo pedido
        if not pedido_id:
            return Response(
                {"error": "Debes proporcionar el ID del pedido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(pedido_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PedidoSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        pedido_data = convertir_fechas(
            serializer.validated_data
        )

        result = pedido_collection.update_one(
            {"_id": object_id},
            {"$set": pedido_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Pedido no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        pedido = pedido_collection.find_one(
            {"_id": object_id}
        )

        pedido = convertir_documento(pedido)

        return Response(pedido, status=status.HTTP_200_OK)

    def delete(self, request, pedido_id):

        try:
            object_id = ObjectId(pedido_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = pedido_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Pedido no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Conductor ------------------


@permission_classes((permissions.AllowAny,))
class ConductorListCreateView(APIView):

    def get(self, request):
        conductores = []

        for documento in conductor_collection.find():

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el conductor
            conductor = convertir_documento(documento)

            # Agregar los datos relacionados
            conductor["usuario"] = usuario

            conductores.append(conductor)

        serializer = ConductorSerializer(conductores, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = ConductorSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        conductores = serializer.validated_data

        # Registrar varios conductores
        if es_lista:
            if not conductores:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = conductor_collection.insert_many(conductores)

            respuesta = []

            for conductor, object_id in zip(conductores, result.inserted_ids):
                conductor["_id"] = object_id
                respuesta.append(convertir_documento(conductor))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo conductor
        conductor = dict(conductores)
        result = conductor_collection.insert_one(conductor)

        conductor["_id"] = result.inserted_id

        conductor = convertir_documento(conductor)

        return Response(
            conductor,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Caso 1: actualizar varios conductores
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del conductor"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = ConductorSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                result = conductor_collection.update_one(
                    {"_id": object_id},
                    {"$set": serializer.validated_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Conductor no encontrado"
                    })
                    continue

                conductor = conductor_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(conductor))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class ConductorDetailView(APIView):

    def get(self, request, conductor_id):

        try:
            object_id = ObjectId(conductor_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el conductor
        documento = conductor_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Conductor no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")
        
        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        conductor = convertir_documento(documento)

        # Agregar los datos relacionados
        conductor["usuario"] = usuario

        serializer = ConductorSerializer(conductor)

        return Response(serializer.data)

    def put(self, request, conductor_id=None):
        data = request.data

        # Caso 2: actualizar un solo conductor
        if not conductor_id:
            return Response(
                {"error": "Debes proporcionar el ID del conductor"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(conductor_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ConductorSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        result = conductor_collection.update_one(
            {"_id": object_id},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Conductor no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        conductor = conductor_collection.find_one(
            {"_id": object_id}
        )

        conductor = convertir_documento(conductor)

        return Response(conductor, status=status.HTTP_200_OK)

    def delete(self, request, conductor_id):

        try:
            object_id = ObjectId(conductor_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = conductor_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Conductor no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Recepción ------------------


@permission_classes((permissions.AllowAny,))
class RecepcionListCreateView(APIView):

    def get(self, request):
        recepciones = []

        for documento in recepcion_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el conductor relacionado
            conductor_id = documento.get("conductor")

            conductor = conductor_collection.find_one({
                "_id": ObjectId(conductor_id)
            }) if conductor_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir el conductor
            if conductor:
                conductor = convertir_documento(conductor)
                conductor = ConductorSerializer(conductor).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir la recepcion
            recepcion = convertir_documento(documento)

            # Agregar los datos relacionados
            recepcion["producto"] = producto
            recepcion["conductor"] = conductor
            recepcion["usuario"] = usuario

            recepciones.append(recepcion)

        serializer = RecepcionSerializer(recepciones, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = RecepcionSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        recepciones = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(recepcion):
            recepcion = dict(recepcion)

            if isinstance(recepcion.get("fRecogida"), date):
                recepcion["fRecogida"] = datetime.combine(
                    recepcion["fRecogida"],
                    time.min
                )

            if isinstance(recepcion.get("hRecogida"), time):
                recepcion["hRecogida"] = recepcion["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fLlegada"), date):
                recepcion["fLlegada"] = datetime.combine(
                    recepcion["fLlegada"],
                    time.min
                )

            if isinstance(recepcion.get("hLlegada"), time):
                recepcion["hLlegada"] = recepcion["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fFabricacion"), date):
                recepcion["fFabricacion"] = datetime.combine(
                    recepcion["fFabricacion"],
                    time.min
                )

            if isinstance(recepcion.get("fVencimiento"), date):
                recepcion["fVencimiento"] = datetime.combine(
                    recepcion["fVencimiento"],
                    time.min
                )

            return recepcion

        # Registrar varias recepciones
        if es_lista:
            if not recepciones:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            recepciones = [
                convertir_fechas(recepcion)
                for recepcion in recepciones
            ]

            result = recepcion_collection.insert_many(recepciones)

            respuesta = []

            for recepcion, object_id in zip(recepciones, result.inserted_ids):
                recepcion["_id"] = object_id
                respuesta.append(convertir_documento(recepcion))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar una sola recepción
        recepcion = convertir_fechas(recepciones)
        result = recepcion_collection.insert_one(recepcion)

        recepcion["_id"] = result.inserted_id

        recepcion = convertir_documento(recepcion)

        return Response(
            recepcion,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(recepcion):
            recepcion = dict(recepcion)

            if isinstance(recepcion.get("fRecogida"), date):
                recepcion["fRecogida"] = datetime.combine(
                    recepcion["fRecogida"],
                    time.min
                )

            if isinstance(recepcion.get("hRecogida"), time):
                recepcion["hRecogida"] = recepcion["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fLlegada"), date):
                recepcion["fLlegada"] = datetime.combine(
                    recepcion["fLlegada"],
                    time.min
                )

            if isinstance(recepcion.get("hLlegada"), time):
                recepcion["hLlegada"] = recepcion["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fFabricacion"), date):
                recepcion["fFabricacion"] = datetime.combine(
                    recepcion["fFabricacion"],
                    time.min
                )

            if isinstance(recepcion.get("fVencimiento"), date):
                recepcion["fVencimiento"] = datetime.combine(
                    recepcion["fVencimiento"],
                    time.min
                )

            return recepcion

        # Caso 1: actualizar varias recepciones
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID de la recepción"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = RecepcionSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                recepcion_data = convertir_fechas(
                    serializer.validated_data
                )

                result = recepcion_collection.update_one(
                    {"_id": object_id},
                    {"$set": recepcion_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Recepción no encontrada"
                    })
                    continue

                recepcion = recepcion_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(recepcion))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)

        

@permission_classes((permissions.AllowAny,))
class RecepcionDetailView(APIView):

    def get(self, request, recepcion_id):

        try:
            object_id = ObjectId(recepcion_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar la recepción
        documento = recepcion_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Recepción no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el conductor relacionado
        conductor_id = documento.get("conductor")

        conductor = conductor_collection.find_one({
            "_id": ObjectId(conductor_id)
        }) if conductor_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir el conductor
        if conductor:
            conductor = convertir_documento(conductor)
            conductor = ConductorSerializer(conductor).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir la recepcion
        recepcion = convertir_documento(documento)

        # Agregar los datos relacionados
        recepcion["producto"] = producto
        recepcion["conductor"] = conductor
        recepcion["usuario"] = usuario

        serializer = RecepcionSerializer(recepcion)

        return Response(serializer.data)

    def put(self, request, recepcion_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(recepcion):
            recepcion = dict(recepcion)

            if isinstance(recepcion.get("fRecogida"), date):
                recepcion["fRecogida"] = datetime.combine(
                    recepcion["fRecogida"],
                    time.min
                )

            if isinstance(recepcion.get("hRecogida"), time):
                recepcion["hRecogida"] = recepcion["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fLlegada"), date):
                recepcion["fLlegada"] = datetime.combine(
                    recepcion["fLlegada"],
                    time.min
                )

            if isinstance(recepcion.get("hLlegada"), time):
                recepcion["hLlegada"] = recepcion["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(recepcion.get("fFabricacion"), date):
                recepcion["fFabricacion"] = datetime.combine(
                    recepcion["fFabricacion"],
                    time.min
                )

            if isinstance(recepcion.get("fVencimiento"), date):
                recepcion["fVencimiento"] = datetime.combine(
                    recepcion["fVencimiento"],
                    time.min
                )

            return recepcion

        # Caso 2: actualizar una sola recepción
        if not recepcion_id:
            return Response(
                {"error": "Debes proporcionar el ID de la recepción"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(recepcion_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecepcionSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        recepcion_data = convertir_fechas(
            serializer.validated_data
        )

        result = recepcion_collection.update_one(
            {"_id": object_id},
            {"$set": recepcion_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Recepción no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        recepcion = recepcion_collection.find_one(
            {"_id": object_id}
        )

        recepcion = convertir_documento(recepcion)

        return Response(recepcion, status=status.HTTP_200_OK)

    def delete(self, request, recepcion_id):

        try:
            object_id = ObjectId(recepcion_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = recepcion_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Recepción no Encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Inventario ------------------


@permission_classes((permissions.AllowAny,))
class InventarioListCreateView(APIView):

    def get(self, request):
        inventarios = []

        for documento in inventario_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el recepcion relacionada
            recepcion_id = documento.get("recepcion")

            recepcion = recepcion_collection.find_one({
                "_id": ObjectId(recepcion_id)
            }) if recepcion_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir la recepcion
            if recepcion:
                recepcion = convertir_documento(recepcion)
                recepcion = RecepcionSerializer(recepcion).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el inventario
            inventario = convertir_documento(documento)

            # Agregar los datos relacionados
            inventario["producto"] = producto
            inventario["recepcion"] = recepcion
            inventario["usuario"] = usuario

            inventarios.append(inventario)

        serializer = InventarioSerializer(inventarios, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = InventarioSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        inventarios = serializer.validated_data

        # Registrar varios inventarios
        if es_lista:
            if not inventarios:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = inventario_collection.insert_many(inventarios)

            respuesta = []

            for inventario, object_id in zip(inventarios, result.inserted_ids):
                inventario["_id"] = object_id
                respuesta.append(convertir_documento(inventario))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo inventario
        inventario = dict(inventarios)
        result = inventario_collection.insert_one(inventario)

        inventario["_id"] = result.inserted_id

        inventario = convertir_documento(inventario)

        return Response(
            inventario,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Caso 1: actualizar varios movimientos
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del movimiento"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = InventarioSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                result = inventario_collection.update_one(
                    {"_id": object_id},
                    {"$set": serializer.validated_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Movimiento no encontrado"
                    })
                    continue

                inventario = inventario_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(inventario))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)



@permission_classes((permissions.AllowAny,))
class InventarioDetailView(APIView):

    def get(self, request, inventario_id):

        try:
            object_id = ObjectId(inventario_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el inventario
        documento = inventario_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Movimiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el recepcion relacionada
        recepcion_id = documento.get("recepcion")

        recepcion = recepcion_collection.find_one({
            "_id": ObjectId(recepcion_id)
        }) if recepcion_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir la recepcion
        if recepcion:
            recepcion = convertir_documento(recepcion)
            recepcion = RecepcionSerializer(recepcion).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el inventario
        inventario = convertir_documento(documento)

        # Agregar los datos relacionados
        inventario["producto"] = producto
        inventario["recepcion"] = recepcion
        inventario["usuario"] = usuario

        serializer = InventarioSerializer(inventario)

        return Response(serializer.data)

    def put(self, request, inventario_id=None):
        data = request.data

        # Caso 2: actualizar un solo movimiento
        if not inventario_id:
            return Response(
                {"error": "Debes proporcionar el ID del movimiento"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(inventario_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InventarioSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        result = inventario_collection.update_one(
            {"_id": object_id},
            {"$set": serializer.validated_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Movimiento no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        inventario = inventario_collection.find_one(
            {"_id": object_id}
        )

        inventario = convertir_documento(inventario)

        return Response(inventario, status=status.HTTP_200_OK)

    def delete(self, request, inventario_id):

        try:
            object_id = ObjectId(inventario_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = inventario_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Movimiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Docking ------------------


@permission_classes((permissions.AllowAny,))
class DockingListCreateView(APIView):

    def get(self, request):
        dockings = []

        for documento in docking_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el pedido relacionado
            pedido_id = documento.get("pedido")

            pedido = pedido_collection.find_one({
                "_id": ObjectId(pedido_id)
            }) if pedido_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir el pedido
            if pedido:
                pedido = convertir_documento(pedido)
                pedido = PedidoSerializer(pedido).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el docking
            docking = convertir_documento(documento)

            # Agregar los datos relacionados
            docking["producto"] = producto
            docking["pedido"] = pedido
            docking["usuario"] = usuario

            dockings.append(docking)

        serializer = DockingSerializer(dockings, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = DockingSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        dockings = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(docking):
            docking = dict(docking)

            if isinstance(docking.get("fInicio"), date):
                docking["fInicio"] = datetime.combine(
                    docking["fInicio"],
                    time.min
                )

            if isinstance(docking.get("hInicio"), time):
                docking["hInicio"] = docking["hInicio"].strftime("%H:%M:%S")

            if isinstance(docking.get("fFin"), date):
                docking["fFin"] = datetime.combine(
                    docking["fFin"],
                    time.min
                )

            if isinstance(docking.get("hFin"), time):
                docking["hFin"] = docking["hFin"].strftime("%H:%M:%S")

            return docking

        # Registrar varios dockings
        if es_lista:
            if not dockings:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            dockings = [
                convertir_fechas(docking)
                for docking in dockings
            ]

            result = docking_collection.insert_many(dockings)

            respuesta = []

            for docking, object_id in zip(dockings, result.inserted_ids):
                docking["_id"] = object_id
                respuesta.append(convertir_documento(docking))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo docking
        docking = convertir_fechas(dockings)
        result = docking_collection.insert_one(docking)

        docking["_id"] = result.inserted_id

        docking = convertir_documento(docking)

        return Response(
            docking,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(docking):
            docking = dict(docking)

            if isinstance(docking.get("fInicio"), date):
                docking["fInicio"] = datetime.combine(
                    docking["fInicio"],
                    time.min
                )

            if isinstance(docking.get("hInicio"), time):
                docking["hInicio"] = docking["hInicio"].strftime("%H:%M:%S")

            if isinstance(docking.get("fFin"), date):
                docking["fFin"] = datetime.combine(
                    docking["fFin"],
                    time.min
                )

            if isinstance(docking.get("hFin"), time):
                docking["hFin"] = docking["hFin"].strftime("%H:%M:%S")

            return docking

        # Caso 1: actualizar varios dockings
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del alistamiento"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = DockingSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                docking_data = convertir_fechas(
                    serializer.validated_data
                )

                result = docking_collection.update_one(
                    {"_id": object_id},
                    {"$set": docking_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Alistamiento no encontrado"
                    })
                    continue

                docking = docking_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(docking))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)

        

@permission_classes((permissions.AllowAny,))
class DockingDetailView(APIView):

    def get(self, request, docking_id):

        try:
            object_id = ObjectId(docking_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el docking
        documento = docking_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Alistamiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el pedido relacionado
        pedido_id = documento.get("pedido")

        pedido = pedido_collection.find_one({
            "_id": ObjectId(pedido_id)
        }) if pedido_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir el pedido
        if pedido:
            pedido = convertir_documento(pedido)
            pedido = PedidoSerializer(pedido).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el docking
        docking = convertir_documento(documento)

        # Agregar los datos relacionados
        docking["producto"] = producto
        docking["pedido"] = pedido
        docking["usuario"] = usuario

        serializer = DockingSerializer(docking)

        return Response(serializer.data)

    def put(self, request, docking_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(docking):
            docking = dict(docking)

            if isinstance(docking.get("fInicio"), date):
                docking["fInicio"] = datetime.combine(
                    docking["fInicio"],
                    time.min
                )

            if isinstance(docking.get("hInicio"), time):
                docking["hInicio"] = docking["hInicio"].strftime("%H:%M:%S")

            if isinstance(docking.get("fFin"), date):
                docking["fFin"] = datetime.combine(
                    docking["fFin"],
                    time.min
                )

            if isinstance(docking.get("hFin"), time):
                docking["hFin"] = docking["hFin"].strftime("%H:%M:%S")

            return docking

        # Caso 2: actualizar un solo alistamiento
        if not docking_id:
            return Response(
                {"error": "Debes proporcionar el ID del alistamiento"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(docking_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DockingSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        docking_data = convertir_fechas(
            serializer.validated_data
        )

        result = docking_collection.update_one(
            {"_id": object_id},
            {"$set": docking_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Alistamiento no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        docking = docking_collection.find_one(
            {"_id": object_id}
        )

        docking = convertir_documento(docking)

        return Response(docking, status=status.HTTP_200_OK)

    def delete(self, request, docking_id):

        try:
            object_id = ObjectId(docking_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = docking_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Alistamiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Alistamiento ------------------


@permission_classes((permissions.AllowAny,))
class AlistamientoListCreateView(APIView):

    def get(self, request):
        alistamientos = []

        for documento in alistamiento_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el pedido relacionado
            pedido_id = documento.get("pedido")

            pedido = pedido_collection.find_one({
                "_id": ObjectId(pedido_id)
            }) if pedido_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir el pedido
            if pedido:
                pedido = convertir_documento(pedido)
                pedido = PedidoSerializer(pedido).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el alistamiento
            alistamiento = convertir_documento(documento)

            # Agregar los datos relacionados
            alistamiento["producto"] = producto
            alistamiento["pedido"] = pedido
            alistamiento["usuario"] = usuario

            alistamientos.append(alistamiento)

        serializer = AlistamientoSerializer(alistamientos, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = AlistamientoSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        alistamientos = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(alistamiento):
            alistamiento = dict(alistamiento)

            if isinstance(alistamiento.get("fInicio"), date):
                alistamiento["fInicio"] = datetime.combine(
                    alistamiento["fInicio"],
                    time.min
                )

            if isinstance(alistamiento.get("hInicio"), time):
                alistamiento["hInicio"] = alistamiento["hInicio"].strftime(
                    "%H:%M:%S")

            if isinstance(alistamiento.get("fFin"), date):
                alistamiento["fFin"] = datetime.combine(
                    alistamiento["fFin"],
                    time.min
                )

            if isinstance(alistamiento.get("hFin"), time):
                alistamiento["hFin"] = alistamiento["hFin"].strftime(
                    "%H:%M:%S")

            return alistamiento

        # Registrar varios alistamientos
        if es_lista:
            if not alistamientos:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            alistamientos = [
                convertir_fechas(alistamiento)
                for alistamiento in alistamientos
            ]

            result = alistamiento_collection.insert_many(alistamientos)

            respuesta = []

            for alistamiento, object_id in zip(alistamientos, result.inserted_ids):
                alistamiento["_id"] = object_id
                respuesta.append(convertir_documento(alistamiento))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo alistamiento
        alistamiento = convertir_fechas(alistamientos)
        result = alistamiento_collection.insert_one(alistamiento)

        alistamiento["_id"] = result.inserted_id

        alistamiento = convertir_documento(alistamiento)

        return Response(
            alistamiento,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(alistamiento):
            alistamiento = dict(alistamiento)

            if isinstance(alistamiento.get("fInicio"), date):
                alistamiento["fInicio"] = datetime.combine(
                    alistamiento["fInicio"],
                    time.min
                )

            if isinstance(alistamiento.get("hInicio"), time):
                alistamiento["hInicio"] = alistamiento["hInicio"].strftime(
                    "%H:%M:%S")

            if isinstance(alistamiento.get("fFin"), date):
                alistamiento["fFin"] = datetime.combine(
                    alistamiento["fFin"],
                    time.min
                )

            if isinstance(alistamiento.get("hFin"), time):
                alistamiento["hFin"] = alistamiento["hFin"].strftime(
                    "%H:%M:%S")

            return alistamiento

        # Caso 1: actualizar varios alistamientos
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del alistamiento"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = AlistamientoSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                alistamiento_data = convertir_fechas(
                    serializer.validated_data
                )

                result = alistamiento_collection.update_one(
                    {"_id": object_id},
                    {"$set": alistamiento_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Alistamiento no encontrado"
                    })
                    continue

                alistamiento = alistamiento_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(alistamiento))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)

@permission_classes((permissions.AllowAny,))
class AlistamientoDetailView(APIView):

    def get(self, request, alistamiento_id):

        try:
            object_id = ObjectId(alistamiento_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el alistamiento
        documento = alistamiento_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Alistamiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el pedido relacionado
        pedido_id = documento.get("pedido")

        pedido = pedido_collection.find_one({
            "_id": ObjectId(pedido_id)
        }) if pedido_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir el pedido
        if pedido:
            pedido = convertir_documento(pedido)
            pedido = PedidoSerializer(pedido).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el alistamiento
        alistamiento = convertir_documento(documento)

        # Agregar los datos relacionados
        alistamiento["producto"] = producto
        alistamiento["pedido"] = pedido
        alistamiento["usuario"] = usuario

        serializer = AlistamientoSerializer(alistamiento)

        return Response(serializer.data)

    def put(self, request, alistamiento_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(alistamiento):
            alistamiento = dict(alistamiento)

            if isinstance(alistamiento.get("fInicio"), date):
                alistamiento["fInicio"] = datetime.combine(
                    alistamiento["fInicio"],
                    time.min
                )

            if isinstance(alistamiento.get("hInicio"), time):
                alistamiento["hInicio"] = alistamiento["hInicio"].strftime(
                    "%H:%M:%S")

            if isinstance(alistamiento.get("fFin"), date):
                alistamiento["fFin"] = datetime.combine(
                    alistamiento["fFin"],
                    time.min
                )

            if isinstance(alistamiento.get("hFin"), time):
                alistamiento["hFin"] = alistamiento["hFin"].strftime(
                    "%H:%M:%S")

            return alistamiento

        # Caso 2: actualizar un solo alistamiento
        if not alistamiento_id:
            return Response(
                {"error": "Debes proporcionar el ID del alistamiento"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(alistamiento_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AlistamientoSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        alistamiento_data = convertir_fechas(
            serializer.validated_data
        )

        result = alistamiento_collection.update_one(
            {"_id": object_id},
            {"$set": alistamiento_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Alistamiento no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        alistamiento = alistamiento_collection.find_one(
            {"_id": object_id}
        )

        alistamiento = convertir_documento(alistamiento)

        return Response(alistamiento, status=status.HTTP_200_OK)

    def delete(self, request, alistamiento_id):

        try:
            object_id = ObjectId(alistamiento_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = alistamiento_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Alistamiento no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ---------------------- Despacho ------------------


@permission_classes((permissions.AllowAny,))
class DespachoListCreateView(APIView):

    def get(self, request):
        despachos = []

        for documento in despacho_collection.find():

            # Buscar el producto relacionado
            producto_id = documento.get("producto")

            producto = producto_collection.find_one({
                "_id": ObjectId(producto_id)
            }) if producto_id else None

            # Buscar el conductor relacionado
            conductor_id = documento.get("conductor")

            conductor = conductor_collection.find_one({
                "_id": ObjectId(conductor_id)
            }) if conductor_id else None

            # Buscar el pedido relacionado
            pedido_id = documento.get("pedido")

            pedido = pedido_collection.find_one({
                "_id": ObjectId(pedido_id)
            }) if pedido_id else None

            # Buscar el usuario relacionado
            usuario_id = documento.get("usuario")

            usuario = usuario_collection.find_one({
                "_id": ObjectId(usuario_id)
            }) if usuario_id else None

            # Convertir el producto
            if producto:
                producto = convertir_documento(producto)
                producto = ProductoSerializer(producto).data

            # Convertir el conductor
            if conductor:
                conductor = convertir_documento(conductor)
                conductor = ConductorSerializer(conductor).data

            # Convertir el pedido
            if pedido:
                pedido = convertir_documento(pedido)
                pedido = PedidoSerializer(pedido).data

            # Convertir el usuario
            if usuario:
                usuario = convertir_documento(usuario)
                usuario = UsuarioSerializer(usuario).data

            # Convertir el despacho
            despacho = convertir_documento(documento)

            # Agregar los datos relacionados
            despacho["producto"] = producto
            despacho["conductor"] = conductor
            despacho["pedido"] = pedido
            despacho["usuario"] = usuario

            despachos.append(despacho)

        serializer = DespachoSerializer(despachos, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Detectar si es un registro o una lista
        es_lista = isinstance(data, list)

        serializer = DespachoSerializer(
            data=data,
            many=es_lista
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        despachos = serializer.validated_data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(despacho):
            despacho = dict(despacho)

            if isinstance(despacho.get("fRecogida"), date):
                despacho["fRecogida"] = datetime.combine(
                    despacho["fRecogida"],
                    time.min
                )

            if isinstance(despacho.get("hRecogida"), time):
                despacho["hRecogida"] = despacho["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fLlegada"), date):
                despacho["fLlegada"] = datetime.combine(
                    despacho["fLlegada"],
                    time.min
                )

            if isinstance(despacho.get("hLlegada"), time):
                despacho["hLlegada"] = despacho["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fFabricacion"), date):
                despacho["fFabricacion"] = datetime.combine(
                    despacho["fFabricacion"],
                    time.min
                )

            if isinstance(despacho.get("fVencimiento"), date):
                despacho["fVencimiento"] = datetime.combine(
                    despacho["fVencimiento"],
                    time.min
                )

            return despacho

        # Registrar varios despachos
        if es_lista:
            if not despachos:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            despachos = [
                convertir_fechas(despacho)
                for despacho in despachos
            ]

            result = despacho_collection.insert_many(despachos)

            respuesta = []

            for despacho, object_id in zip(despachos, result.inserted_ids):
                despacho["_id"] = object_id
                respuesta.append(convertir_documento(despacho))

            return Response(
                respuesta,
                status=status.HTTP_201_CREATED
            )

        # Registrar un solo despacho
        despacho = convertir_fechas(despachos)
        result = despacho_collection.insert_one(despacho)

        despacho["_id"] = result.inserted_id

        despacho = convertir_documento(despacho)

        return Response(
            despacho,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(despacho):
            despacho = dict(despacho)

            if isinstance(despacho.get("fRecogida"), date):
                despacho["fRecogida"] = datetime.combine(
                    despacho["fRecogida"],
                    time.min
                )

            if isinstance(despacho.get("hRecogida"), time):
                despacho["hRecogida"] = despacho["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fLlegada"), date):
                despacho["fLlegada"] = datetime.combine(
                    despacho["fLlegada"],
                    time.min
                )

            if isinstance(despacho.get("hLlegada"), time):
                despacho["hLlegada"] = despacho["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fFabricacion"), date):
                despacho["fFabricacion"] = datetime.combine(
                    despacho["fFabricacion"],
                    time.min
                )

            if isinstance(despacho.get("fVencimiento"), date):
                despacho["fVencimiento"] = datetime.combine(
                    despacho["fVencimiento"],
                    time.min
                )

            return despacho

        # Caso 1: actualizar varios despachos
        if isinstance(data, list):

            if not data:
                return Response(
                    {"error": "La lista no puede estar vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            actualizados = []
            errores = []

            for indice, item in enumerate(data):
                if not isinstance(item, dict):
                    errores.append({
                        "indice": indice,
                        "error": "Cada registro debe ser un objeto"
                    })
                    continue

                item = dict(item)
                id_actual = item.pop("id", None)

                if not id_actual:
                    errores.append({
                        "indice": indice,
                        "error": "Falta el ID del despacho"
                    })
                    continue

                try:
                    object_id = ObjectId(id_actual)
                except (InvalidId, TypeError):
                    errores.append({
                        "indice": indice,
                        "error": "ID inválido"
                    })
                    continue

                serializer = DespachoSerializer(data=item)

                if not serializer.is_valid():
                    errores.append({
                        "indice": indice,
                        "errores": serializer.errors
                    })
                    continue

                # Convertir la fecha antes de guardar en MongoDB
                despacho_data = convertir_fechas(
                    serializer.validated_data
                )

                result = despacho_collection.update_one(
                    {"_id": object_id},
                    {"$set": despacho_data}
                )

                if result.matched_count == 0:
                    errores.append({
                        "indice": indice,
                        "error": "Despacho no encontrado"
                    })
                    continue

                despacho = despacho_collection.find_one(
                    {"_id": object_id}
                )

                actualizados.append(convertir_documento(despacho))

            return Response({
                "total_actualizados": len(actualizados),
                "total_errores": len(errores),
                "actualizados": actualizados,
                "errores": errores
            }, status=status.HTTP_200_OK)

@permission_classes((permissions.AllowAny,))
class DespachoDetailView(APIView):

    def get(self, request, despacho_id):

        try:
            object_id = ObjectId(despacho_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el despacho
        documento = despacho_collection.find_one({
            "_id": object_id
        })

        if not documento:
            return Response(
                {"error": "Despacho no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar el producto relacionado
        producto_id = documento.get("producto")

        producto = producto_collection.find_one({
            "_id": ObjectId(producto_id)
        }) if producto_id else None

        # Buscar el conductor relacionado
        conductor_id = documento.get("conductor")

        conductor = conductor_collection.find_one({
            "_id": ObjectId(conductor_id)
        }) if conductor_id else None

        # Buscar el pedido relacionado
        pedido_id = documento.get("pedido")

        pedido = pedido_collection.find_one({
            "_id": ObjectId(pedido_id)
        }) if pedido_id else None

        # Buscar el usuario relacionado
        usuario_id = documento.get("usuario")

        usuario = usuario_collection.find_one({
            "_id": ObjectId(usuario_id)
        }) if usuario_id else None

        # Convertir el producto
        if producto:
            producto = convertir_documento(producto)
            producto = ProductoSerializer(producto).data

        # Convertir el conductor
        if conductor:
            conductor = convertir_documento(conductor)
            conductor = ConductorSerializer(conductor).data

        # Convertir el pedido
        if pedido:
            pedido = convertir_documento(pedido)
            pedido = PedidoSerializer(pedido).data

        # Convertir el usuario
        if usuario:
            usuario = convertir_documento(usuario)
            usuario = UsuarioSerializer(usuario).data

        # Convertir el despacho
        despacho = convertir_documento(documento)

        # Agregar los datos relacionados
        despacho["producto"] = producto
        despacho["conductor"] = conductor
        despacho["pedido"] = pedido
        despacho["usuario"] = usuario

        serializer = DespachoSerializer(despacho)

        return Response(serializer.data)

    def put(self, request, despacho_id=None):
        data = request.data

        # Convertir fechas para que sean compatibles con BSON
        def convertir_fechas(despacho):
            despacho = dict(despacho)

            if isinstance(despacho.get("fRecogida"), date):
                despacho["fRecogida"] = datetime.combine(
                    despacho["fRecogida"],
                    time.min
                )

            if isinstance(despacho.get("hRecogida"), time):
                despacho["hRecogida"] = despacho["hRecogida"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fLlegada"), date):
                despacho["fLlegada"] = datetime.combine(
                    despacho["fLlegada"],
                    time.min
                )

            if isinstance(despacho.get("hLlegada"), time):
                despacho["hLlegada"] = despacho["hLlegada"].strftime(
                    "%H:%M:%S")

            if isinstance(despacho.get("fFabricacion"), date):
                despacho["fFabricacion"] = datetime.combine(
                    despacho["fFabricacion"],
                    time.min
                )

            if isinstance(despacho.get("fVencimiento"), date):
                despacho["fVencimiento"] = datetime.combine(
                    despacho["fVencimiento"],
                    time.min
                )

            return despacho

        # Caso 2: actualizar un solo despacho
        if not despacho_id:
            return Response(
                {"error": "Debes proporcionar el ID del despacho"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            object_id = ObjectId(despacho_id)
        except (InvalidId, TypeError):
            return Response(
                {"error": "ID inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DespachoSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convertir la fecha antes de guardar en MongoDB
        despacho_data = convertir_fechas(
            serializer.validated_data
        )

        result = despacho_collection.update_one(
            {"_id": object_id},
            {"$set": despacho_data}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Despacho no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        despacho = despacho_collection.find_one(
            {"_id": object_id}
        )

        despacho = convertir_documento(despacho)

        return Response(despacho, status=status.HTTP_200_OK)

    def delete(self, request, despacho_id):

        try:
            object_id = ObjectId(despacho_id)
        except InvalidId:
            return Response(
                {"error": "ID Inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = despacho_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Despacho no Encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
