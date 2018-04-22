from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response

from .gcloud import predict

import json
from PIL import Image
from io import BytesIO
import base64
import numpy as np

from .gcloud import predict

from rest_framework import status


import re
import base64
from io import BytesIO

image_dims = (50,30)


@api_view(['POST'])
def get_building(request):

    data_uri = json.loads(request.body.decode("utf-8"))['image']

    base_64 = re.sub('^data:image/.+;base64,', '', data_uri)

    image = Image.open(BytesIO(base64.b64decode(base_64)))
    resized_image = image.resize(image_dims)
    reshaped_image = np.array(list(resized_image.getdata()))
    reshaped_image = reshaped_image.reshape(50, 30, 3)

    building = predict((reshaped_image.tolist()))

    return Response(building, status=status.HTTP_200_OK)







