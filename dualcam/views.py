from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dualcam import merge_request, timestamp_convert
from dualcam.models import File, Record, FileRecord, DeviceProperty, Property
from dualcam.serializers import FIELDS_OF_FILE, FIELDS_OF_FILE_RECORDS, FIELDS_OF_RECORD
from dualcam.serializers import FileSerializer, RecordSerializer, FileRecordSerializer
from dualcam.serializers import DevicePropertySerializer, PropertySerializer

UTC = 'UTC'

AMERICA_BOGOTA = 'America/Bogota'

QUERY_CONFIG = ["type"]

UTF8 = 'utf-8'


# Create your views here.
class FileApi(APIView):

    def get(self, request, *args, **kwargs):
        # print('file/', request, args, kwargs)
        file_repo = File.objects
        many_files = True
        no_kwargs = kwargs is None or len(kwargs) <= 0
        no_query_params = request is None or not hasattr(request, "query_params")
        if no_kwargs and no_query_params:
            files = file_repo.all()
        else:
            if not no_kwargs:
                files = file_repo.filter(**kwargs)
            elif not no_query_params:
                query_params_dict = dict(request.query_params)
                query_type = False
                if "type" in list(query_params_dict.keys()):
                    query_type = query_params_dict["type"]
                    if type(query_type) is list:
                        query_type = query_type.pop()
                query_params = {k: v if type(v) is not list else v.pop()
                                for k, v in query_params_dict.items() if k not in QUERY_CONFIG}
                files = file_repo.filter(**query_params)
                if query_type:
                    if query_type == "count":
                        count_response = {"num": files.count()}
                        return Response(count_response, status=status.HTTP_200_OK)
                    if query_type == "max":
                        id = 'file_id'
                        max_values = files.order_by('-%s' % id).values('%s' % id)
                        last_value = None
                        if max_values is not None and len(max_values) > 0:
                            last_value = dict(max_values.first())[id]
                        max_response = {"max": last_value}
                        return Response(max_response, status=status.HTTP_200_OK)
            else:
                files = file_repo.get(**kwargs)
                many_files = False
        serializer = FileSerializer(files, many=many_files)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print('post:file', request.data, args, kwargs)
        if request is None or request.data is None or len(request.data) <= 0:
            response_data = {"error": "No se ha recibido ningún dato."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        file_data = merge_request(request.data, FIELDS_OF_FILE)
        serializer = FileSerializer(data=file_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as file_save_e:
            return Response(file_save_e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            # else:~
            #     file_records = file_record_repo.get(**kwargs)
            #     many_records = False
        serializer = FileRecordSerializer(file_records, many=many_records)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print('post:file_record', request.data, args, kwargs)
        if request is None or request.data is None or len(request.data) <= 0:
            response_data = {"error": "No se ha recibido ningún dato."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        response_extra = None
        if kwargs is not None and len(kwargs) > 0:
            if "file_key" in kwargs:
                file_key = kwargs["file_key"]
                file_repo = File.objects
                try:
                    files = file_repo.get(**{"file_id": file_key})
                    if files is None:
                        response_data = {"error": "File not found"}
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                except Exception as file_repo_e:
                    response_data = {"error": "File not found", "message": str(file_repo_e)}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                offset_default = {"record_offset": 0}
                content_block_convert = {"content_block": lambda v: bytearray(v, UTF8)}
                record_data = merge_request(request_data, FIELDS_OF_RECORD,
                                            defaults=offset_default, convert=content_block_convert)
                serializer = RecordSerializer(data=record_data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                request_data = {"file_key": file_key}
                try:
                    if "record_id" not in FIELDS_OF_RECORD:
                        response_data = {"error": "record_id not found"}
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    response_extra = Response(serializer.data, status=status.HTTP_201_CREATED)
                    request_data["record_key"] = serializer.data["record_id"]
                except Exception as record_save_e:
                    return Response(str(record_save_e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                response_data = {"error": "Method not allowed"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        file_record_data = merge_request(request_data, FIELDS_OF_FILE_RECORDS)
        serializer = FileRecordSerializer(data=file_record_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            response_data = serializer.data
            if response_extra is not None:
                response_data["extra"] = response_extra.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as file_record_save_e:
            return Response(file_record_save_e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DevicePropertyApi(APIView):

    def get(self, request, *args, **kwargs):
        device_property_repo = DeviceProperty.objects
        many_properties = True
        no_kwargs = kwargs is None or len(kwargs) <= 0
        no_query_params = request is None or not hasattr(request, "query_params")
        if no_kwargs and no_query_params:
            device_properties = device_property_repo.all()
        else:
            if not no_kwargs:
                device_properties = device_property_repo.filter(**kwargs)
            elif not no_query_params:
                query_params_dict = dict(request.query_params)
                query_type = False
                if "type" in list(query_params_dict.keys()):
                    query_type = query_params_dict["type"]
                    if type(query_type) is list:
                        query_type = query_type.pop()
                query_params = {k: v if type(v) is not list else v.pop()
                                for k, v in query_params_dict.items() if k not in QUERY_CONFIG}
                bytearray_convert = {"parent_event": lambda v: bytearray(v, UTF8),
                                     "property_stamp": lambda v: timestamp_convert(v, UTC)}
                fields_in_device_properties = list(query_params.keys())
                query_params = merge_request(query_params, fields_in_device_properties, convert=bytearray_convert)
                device_properties = device_property_repo.filter(**query_params)
                if query_type:
                    if query_type == "count":
                        count_response = {"num": device_properties.count()}
                        return Response(count_response, status=status.HTTP_200_OK)
            else:
                device_properties = device_property_repo.get(**kwargs)
                many_properties = False
        serializer = DevicePropertySerializer(device_properties, many=many_properties)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PropertyApi(APIView):

    def get(self, request, *args, **kwargs):
        property_repo = Property.objects
        many_properties = True
        no_kwargs = kwargs is None or len(kwargs) <= 0
        no_query_params = request is None or not hasattr(request, "query_params")
        if no_kwargs and no_query_params:
            properties = property_repo.all()
        else:
            if not no_kwargs:
                properties = property_repo.filter(**kwargs)
            elif not no_query_params:
                query_params_dict = dict(request.query_params)
                query_type = False
                if "type" in list(query_params_dict.keys()):
                    query_type = query_params_dict["type"]
                    if type(query_type) is list:
                        query_type = query_type.pop()
                query_params = {k: v if type(v) is not list else v.pop()
                                for k, v in query_params_dict.items() if k not in QUERY_CONFIG}
                bytearray_convert = {"event_key": lambda v: bytearray(v, UTF8),
                                     "property_value": lambda v: bytearray(v, UTF8)}
                fields_in_device_properties = list(query_params.keys())
                query_params = merge_request(query_params, fields_in_device_properties, convert=bytearray_convert)
                properties = property_repo.filter(**query_params)
                if query_type:
                    if query_type == "count":
                        count_response = {"num": properties.count()}
                        return Response(count_response, status=status.HTTP_200_OK)
                    if query_type == "max":
                        id = 'property_id'
                        max_values = properties.order_by('-%s' % id).values('%s' % id)
                        last_value = None
                        if max_values is not None and len(max_values) > 0:
                            last_value = dict(max_values.first())[id]
                        max_response = {"max": last_value}
                        return Response(max_response, status=status.HTTP_200_OK)
            else:
                properties = property_repo.get(**kwargs)
                many_properties = False
        serializer = PropertySerializer(properties, many=many_properties)
        return Response(serializer.data, status=status.HTTP_200_OK)
