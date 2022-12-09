# Create your views here.
from django.shortcuts import get_object_or_404,render
from serverui.models import Music
from serverui.models import fun_raw_sql_query, fun_sql_cursor_update
from serverui.serializers import MusicSerializer, MusicSerializerV1

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action


# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
    # /api/music/{pk}/detail/
    @action(detail=True,methods=['get'])
    def detail(self, request, pk=None):
        music = get_object_or_404(Music, pk=pk)
        result = {
            'singer': music.singer,
            'song': music.song
        }

        return Response(result, status=status.HTTP_200_OK)

    # /api/music/all_singer/
    @action(detail=True,methods=['get'],url_path='all_singer')
    def all_singer(self, request):
        music = Music.objects.values_list('singer', flat=True).distinct()
        return Response(music, status=status.HTTP_200_OK)

    # /api/music/raw_sql_query/
    @action(detail=True,methods=['get'])
    def raw_sql_query(self, request):
        song = request.query_params.get('song', None)
        music = fun_raw_sql_query(song=song)
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /api/music/{pk}/sql_cursor_update/
    @action(detail=True,methods=['put'])
    def sql_cursor_update(self, request, pk=None):
        song = request.data.get('song', None)
        if song:
            music = fun_sql_cursor_update(song=song, pk=pk)
            return Response(music, status=status.HTTP_200_OK)

    # /api/music/version_api/
    @action(detail=True,methods=['get'])
    def version_api(self, request):
        music = Music.objects.all()
        if self.request.version == '1.0':
            serializer = MusicSerializerV1(music, many=True)
        else:
            serializer = MusicSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False,methods=['get'],url_path='musics')
    def index(self,request):
        musics=Music.objects.all()

        return render(request, "musics/index.html",{"musics":musics})
