import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dualcam.models import File, Record, FileRecord
from dualcam.serializers import FileSerializer, RecordSerializer, FileRecordSerializer, FIELDS_OF_FILE


# Create your views here.
class FileApi(APIView):

    def get(self, request, *args, **kwargs):
        # print('file/', request, args, kwargs)
        file_repo = File.objects
        many_files = True
        if kwargs is None or len(kwargs) <= 0:
            files = file_repo.all()
        else:
            if "file_id" not in kwargs:
                files = file_repo.filter(**kwargs)
            else:
                files = file_repo.get(**kwargs)
                many_files = False
        serializer = FileSerializer(files, many=many_files)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print('post:file', request.data, args, kwargs)
        if request is None or request.data is None or len(request.data) <= 0:
            return Response(json.dumps({"error": "No se ha recibido ningún dato."}), status=status.HTTP_400_BAD_REQUEST)
        fields_data = dict.fromkeys(FIELDS_OF_FILE, "")
        data = {}
        return Response(json.loads(json.dumps({"message": data})), status=status.HTTP_202_ACCEPTED)


class RecordApi(APIView):

    def get(self, request, *args, **kwargs):
        record_repo = Record.objects
        many_records = True
        if kwargs is None or len(kwargs) <= 0:
            records = record_repo.all()
        else:
            if "record_id" not in kwargs:
                records = record_repo.filter(**kwargs)
            else:
                records = record_repo.get(**kwargs)
                many_records = False
        serializer = RecordSerializer(records, many=many_records)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileRecordApi(APIView):

    def get(self, request, *args, **kwargs):
        file_record_repo = FileRecord.objects
        many_records = True
        if kwargs is None or len(kwargs) <= 0:
            file_records = file_record_repo.all()
        else:
            # if "file_key" not in kwargs:
            file_records = file_record_repo.filter(**kwargs)
            # else:
            #     file_records = file_record_repo.get(**kwargs)
            #     many_records = False
        serializer = FileRecordSerializer(file_records, many=many_records)
        return Response(serializer.data, status=status.HTTP_200_OK)

