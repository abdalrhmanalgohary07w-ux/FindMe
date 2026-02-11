from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MissingPerson
from .serializers import MissingPersonSerializer
from .services import FaceRecognitionService

class MissingPersonViewSet(viewsets.ModelViewSet):
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'status']
    search_fields = ['full_name', 'last_seen_location']
    ordering_fields = ['created_at', 'age']

    @action(detail=False, methods=['post'], url_path='search-by-image')
    def search_by_image(self, request):
        """
        Endpoint to receive an image and search for similar people
        """
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Image required for search'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 1. Save temp image
            temp_path = FaceRecognitionService.save_temp_image(image_file)

            # 2. Find matches
            matched_person_ids = FaceRecognitionService.find_matches(temp_path)

            # 3. Fetch full objects from DB
            matched_persons = MissingPerson.objects.filter(id__in=matched_person_ids)
            serializer = self.get_serializer(matched_persons, many=True)

            return Response({
                'message': f'Search completed. Found {len(matched_persons)} matches.',
                'results': serializer.data
            })

        except Exception as e:
            return Response({
                'error': 'An error occurred during facial recognition.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

