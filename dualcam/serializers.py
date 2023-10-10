from rest_framework import serializers
from dualcam.models import File, Record, FileRecord, DeviceProperty, Property

FIELDS_OF_RECORD = ["record_id", "content_block", "record_stamp", "record_offset"]

FIELDS_OF_FILE = ["file_id", "device_key", "file_stamp", "mime_type", "temp_file", "orientation"]

FIELDS_OF_FILE_RECORDS = ['file_key', 'record_key']

FIELDS_OF_DEVICE_PROPERTIES = ['device_key', 'property_key', 'property_stamp', 'parent_event']

FIELDS_OF_PROPERTIES = ['event_key', 'property_value', 'property_id']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = FIELDS_OF_FILE


class FileRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRecord
        fields = FIELDS_OF_FILE_RECORDS


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = FIELDS_OF_RECORD


class DevicePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceProperty
        fields = FIELDS_OF_DEVICE_PROPERTIES


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = FIELDS_OF_PROPERTIES
