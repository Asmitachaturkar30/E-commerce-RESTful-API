import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.core.exceptions import ValidationError
from django.utils import timezone

@csrf_exempt
def get_all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'productId': product.productId,
                'productName': product.productName,
                'price': str(product.price),
                'stockQuantity': product.stockQuantity,
                'imageUrl': product.imageUrl,
                'dateAdded': product.dateAdded.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = {
            'productId': product.productId,
            'productName': product.productName,
            'price': str(product.price),
            'stockQuantity': product.stockQuantity,
            'imageUrl': product.imageUrl,
            'dateAdded': product.dateAdded.strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                productId=data['productId'],
                productName=data['productName'],
                price=data['price'],
                stockQuantity=data.get('stockQuantity', 0),
                imageUrl=data.get('imageUrl', None),
                dateAdded=timezone.now()
            )
            return JsonResponse({'message': 'Product created successfully', 'productId': product.productId}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if request.method == 'PUT':
            try:
                data = json.loads(request.body)
                product.productId = data.get('productId', product.productId)
                product.productName = data.get('productName', product.productName)
                product.price = data.get('price', product.price)
                product.stockQuantity = data.get('stockQuantity', product.stockQuantity)
                product.imageUrl = data.get('imageUrl', product.imageUrl)
                product.save()
                return JsonResponse({'message': 'Product updated successfully', 'productId': product.productId})
            except KeyError:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            except ValidationError as e:
                return JsonResponse({'error': e.message}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if request.method == 'DELETE':
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully', 'id': pk})
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)
