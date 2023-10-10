from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _

SUFFIX = ''
# '_temp'


# Create your models here.
class File(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    device_key = models.CharField(max_length=255)
    file_stamp = models.DateTimeField(auto_now_add=True)

    class MimeTypesInFile(models.TextChoices):
        IMAGE_JPEG = "image/jpeg", _("image (jpeg)")
        OCTET_STREAM = "application/octet-stream", _("video h265 (octect-stream)")
    mime_type = models.CharField(max_length=255, choices=MimeTypesInFile.choices, default=MimeTypesInFile.IMAGE_JPEG)
    temp_file = models.CharField(max_length=255)

    class OrientationInFile(models.TextChoices):
        FRONT = "front", _('Front')
        REAR = "rear", _('Reverse')
    orientation = models.CharField(max_length=255, choices=OrientationInFile.choices, default=OrientationInFile.REAR)

    class Meta:
        db_table = 'files{0}'.format(SUFFIX)


class Record(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    content_block = models.BinaryField(editable=True)
    record_stamp = models.DateTimeField(auto_now_add=True)
    record_offset = models.IntegerField(default=0)

    class Meta:
        db_table = 'records{0}'.format(SUFFIX)


class FileRecord(models.Model):
    file_key = models.ForeignKey(File, db_column='file_key', to_field='file_id', on_delete=CASCADE)
    record_key = models.ForeignKey(Record, db_column='record_key', to_field='record_id', on_delete=CASCADE)

    _id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'file_records{0}'.format(SUFFIX)


class Device(models.Model):
    device_id = models.CharField(max_length=255,primary_key=True)
    device_model = models.CharField(max_length=255)
    device_label = models.CharField(max_length=255)

    class Meta:
        db_table = 'device{0}'.format(SUFFIX)


class Property(models.Model):
    event_key = models.BinaryField(editable=True)
    property_value = models.BinaryField(editable=True)
    property_id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'properties{0}'.format(SUFFIX)


class DeviceProperty(models.Model):
    device_key = models.ForeignKey(Device, db_column='device_key', to_field='device_id', on_delete=CASCADE)
    property_key = models.ForeignKey(Property, db_column='property_key', to_field='property_id', on_delete=CASCADE)
    property_stamp = models.DateTimeField(auto_now_add=True)
    parent_event = models.BinaryField(editable=True)
    _id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'device_properties{0}'.format(SUFFIX)
