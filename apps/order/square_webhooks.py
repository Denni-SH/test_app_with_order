from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apps.order.services.square import SquareService


@csrf_exempt
@api_view(['POST'])
def order_payment_webhook(request):
    payload = request.data

    try:
        square_service = SquareService()
        square_service.handle_payment_webhook(payload)
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
