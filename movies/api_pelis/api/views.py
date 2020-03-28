from django.shortcuts import render
from .models import Pelicula
from .serializers import PeliculaSerializer
from rest_framework import viewsets, views, filters
from .models import Pelicula, PeliculaFavorita
from .serializers import PeliculaSerializer, PeliculaFavoritaSerializer

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class PeliculaViewSet(viewsets.ModelViewSet):
  queryset = Pelicula.objects.all()
  serializer_class = PeliculaSerializer
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['titulo']
  ordering_fields = ['favoritos']

class MarcarPeliculaFavorita(views.APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

 
  def post(self, request):

    pelicula = get_object_or_404(
      Pelicula, id=self.request.data.get('id', 0)
    )

    favorita, created = PeliculaFavorita.objects.get_or_create(
      pelicula=pelicula, usuario=request.user
    )

    
    content = {
      'id': pelicula.id,
      'favorita': True
    }

    
    if not created:
      favorita.delete()
      content['favorita'] = False

    return Response(content)

class ListarPeliculasFavoritas(views.APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]



  def get(self, request):

    peliculas_favoritas = PeliculaFavorita.objects.filter(
      usuario=request.user)
    serializer = PeliculaFavoritaSerializer(
      peliculas_favoritas, many=True)

    return Response(serializer.data)


