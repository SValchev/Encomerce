from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.serializer import StatusReportSerializer
from main.models import Status

class StatusCollection(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    queryset = Status.objects.all()
    serializer_class = StatusReportSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class StatusMember(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):

    queryset = Status.objects.all()
    serializer_class = StatusReportSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
