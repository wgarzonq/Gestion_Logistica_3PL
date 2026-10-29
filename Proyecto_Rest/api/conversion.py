from bson import ObjectId
from datetime import date, datetime, time

def convertir_documento(documento):
    if documento is None:
        return None

    documento = dict(documento)

    if "_id" in documento:
        documento["id"] = str(documento.pop("_id"))

    for clave, valor in documento.items():
        if isinstance(valor, ObjectId):
            documento[clave] = str(valor)

        elif isinstance(valor, (datetime, date)):
            documento[clave] = valor.isoformat()

        elif isinstance(valor, dict):
            documento[clave] = convertir_documento(valor)

        elif isinstance(valor, list):
            documento[clave] = [
                convertir_documento(item)
                if isinstance(item, dict)
                else str(item) if isinstance(item, ObjectId)
                else item.isoformat()
                if isinstance(item, (datetime, date))
                else item
                for item in valor
            ]

    return documento