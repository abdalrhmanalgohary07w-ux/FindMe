import os
from django.conf import settings
from deepface import DeepFace
from .models import MissingPerson

class FaceRecognitionService:
    @staticmethod
    def save_temp_image(image_file):
        """Saves a temporary image for processing"""
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_search.jpg')
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
            
        with open(temp_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        return temp_path

    @staticmethod
    def find_matches(image_path, threshold=0.55):
        """Searches for matches in the face database"""
        db_path = os.path.join(settings.MEDIA_ROOT, 'missing_persons')
        
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        if not os.listdir(db_path):
            return []

        try:
            results = DeepFace.find(
                img_path=image_path, 
                db_path=db_path, 
                enforce_detection=False,
                model_name='Facenet512',
                distance_metric='cosine',
                detector_backend='opencv'
            )

            matched_person_ids = []
            if len(results) > 0:
                df = results[0]
                if not df.empty:
                    matches = df[df['distance'] < threshold]
                    
                    for index, row in matches.iterrows():
                        image_path_match = row['identity']
                        filename = os.path.basename(image_path_match)
                        # Find the person in DB based on image filename
                        db_matches = MissingPerson.objects.filter(image__icontains=filename)
                        for person in db_matches:
                            if person.id not in matched_person_ids:
                                matched_person_ids.append(person.id)
            
            return matched_person_ids
        except Exception as e:
            print(f"DeepFace Search Error: {str(e)}")
            raise e
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
