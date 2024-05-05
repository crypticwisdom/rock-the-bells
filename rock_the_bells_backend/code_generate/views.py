import secrets

from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from io import BytesIO
import qrcode
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import CodeModel
from .serializers import CodeSerializer


# Create your views here.


class GetCodeView(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        url_ = data.get('data', None)

        if url_ is None:
            return Response({"error": "Can't find data to be inserted in the QR Code"}, status=HTTP_400_BAD_REQUEST)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add redirect URL if available
        slug = secrets.token_urlsafe(40)
        code_instance = CodeModel.objects.create(slug=slug)

        qr_data = None
        if code_instance:
            qr_data = f"{url_}"
            code_instance.data = url_


        # Add data to the QR code
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer)
        image_file = ContentFile(buffer.getvalue())

        # Save the image file to the event
        code_instance.qr_code.save(f'qr_code_{code_instance.slug}.png', image_file)
        serialized_data = CodeSerializer(code_instance, context={'request': request}, many=False).data
        return Response({"status_message": "success", "message": "Code has been created", "data": serialized_data})

