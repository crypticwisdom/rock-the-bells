from django.db import models

# Create your models here.


class CodeModel(models.Model):
    slug = models.CharField(max_length=290, null=True, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True, )
    data = models.CharField(max_length=290, null=True, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"qrcode - {self.slug}"
