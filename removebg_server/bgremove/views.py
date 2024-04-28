from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .obj_yolo import BackgroundRemoval
from django.http import HttpResponse
from rest_framework.decorators import api_view
from PIL import Image
from io import BytesIO


# Create your views here.
@api_view(['POST'])
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        
        image = request.FILES['image']
        
        # save the image to dataset folder
        image_path = f'bgremove/dataset/input.jpg'
        # save the image to image_path if not exists then create
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        # with open(image_path, 'wb') as f:
        #     f.write(requests.get(image_url).content)
                
        return Response({'message': 'Image uploaded successfully!'})
    

@api_view(['GET'])
def remove_background(request):
    if request.method == 'GET':
        # Create an instance of the BackgroundRemoval class 
        bg_remove = BackgroundRemoval()
        # Call the remove_background method
        bg_remove.remove_background()
        
        with open('bgremove/output/result.jpg', 'rb') as img_file:
            image = Image.open(img_file)
            # Convert image to bytes
            img_byte_array = BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array = img_byte_array.getvalue()

        # Return the image in the response
        return HttpResponse(img_byte_array, content_type='image/jpeg')
        # return Response({'message': 'Background removed successfully!'})
# @api_view(['GET'])
# def remove_background(request):
#     if request.method == 'GET':
#         # Create an instance of the BackgroundRemoval class
#         bg_remove = BackgroundRemoval()
#         # Call the remove_background method
#         bg_remove.remove_background()
#         img = open('bgremove/output/result.jpg', 'rb')

#         response = FileResponse(img)

#         return Response({'message': 'Background removed successfully!', 'image': response, 'status': 200})
#         # return Response({'message': 'Background removed successfully!'})