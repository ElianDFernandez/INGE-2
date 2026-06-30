import mercadopago
from django.conf import settings

def get_mercadopago_sdk():
    # Inicializa el SDK usando la credencial guardada en tu configuración
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    return sdk