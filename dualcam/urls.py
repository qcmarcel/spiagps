from django.urls import path

from dualcam.models import File
from dualcam.views import FileApi, RecordApi, FileRecordApi, DevicePropertyApi, PropertyApi

urlpatterns = [
    path('file/', FileApi.as_view()),
    path('file/<file_id>', FileApi.as_view()),
    path('record/<record_id>', RecordApi.as_view()),
    # path('records/', FileRecordApi.as_view()),
    path('records/<file_key>', FileRecordApi.as_view()),
    path('device_properties/', DevicePropertyApi.as_view()),
    path('properties/', PropertyApi.as_view())
]
