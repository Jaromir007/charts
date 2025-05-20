from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from .utils import parse_chordspro

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs): 
        chordspro_text = request.data_get('chordspro_text')
        parsed_json = parse_chordspro(chordspro_text)

        serializer = self.get_serizlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = serializer.data
        response_data['parsed'] = parsed_json

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
