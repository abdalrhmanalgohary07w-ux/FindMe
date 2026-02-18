import os
import tempfile
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MissingPerson
from .serializers import MissingPersonSerializer
from django.conf import settings

# Attempt to import DeepFace
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    import traceback
    DEEPFACE_ERROR = f"{str(e)}\n{traceback.format_exc()}"
    DEEPFACE_AVAILABLE = False
    print(f"Warning: DeepFace could not be loaded. Error: {str(e)}")

class MissingPersonViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer

    @action(detail=False, methods=['post'], url_path='search-by-image')
    def search_by_image(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not DEEPFACE_AVAILABLE:
            return Response({
                'error': 'Image search engine is currently offline on the server',
                'detail': globals().get('DEEPFACE_ERROR', 'Unknown error during import')
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        uploaded_image = request.FILES['image']
        
        # Save search image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in uploaded_image.chunks():
                temp_file.write(chunk)
            search_image_path = temp_file.name

        matches = []
        try:
            # Get all persons who have an image
            persons_with_images = MissingPerson.objects.exclude(image='')
            
            comparison_results = []
            for person in persons_with_images:
                try:
                    target_image_path = person.image.path
                    
                    # Improved verification parameters for higher accuracy
                    result = DeepFace.verify(
                        img1_path=search_image_path,
                        img2_path=target_image_path,
                        enforce_detection=True, # Ensure a face is actually found
                        model_name='Facenet512',
                        detector_backend='retinaface', # MUCH more accurate than opencv
                        distance_metric='cosine',
                        align=True
                    )
                    
                    distance = result['distance']
                    # Facenet512 cosine threshold is typically around 0.3. 
                    # 0.4 is a good balance for search candidates.
                    if distance < 0.45: 
                        comparison_results.append({
                            'person': person,
                            'distance': distance,
                            'verified': result['verified']
                        })
                        
                except Exception as e:
                    # If no face detected in one of the images, it might throw an error with enforce_detection=True
                    print(f"Skipping comparison for person {person.id}: {str(e)}")
                    continue

            # Sort results: smallest distance (most similar) first
            comparison_results.sort(key=lambda x: x['distance'])
            
            # Take top 5 candidates
            final_matches = [res['person'] for res in comparison_results[:5]]

            serializer = self.get_serializer(final_matches, many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"CRITICAL ERROR during search: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': f"Search failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Clean up temporary file
            if os.path.exists(search_image_path):
                os.remove(search_image_path)
