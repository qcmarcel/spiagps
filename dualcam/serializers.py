from rest_framework import serializers
from dualcam.models import File, Record, FileRecord

FIELDS_OF_RECORD = ["content_block", "record_stamp", "record_offset"]

FIELDS_OF_FILE = ["device_key", "file_stamp", "mime_type", "temp_file", "orientation"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = FIELDS_OF_FILE


class FileRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRecord
        fields = [
            # "file_key",
            "record_key"
        ]

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = FIELDS_OF_RECORD
