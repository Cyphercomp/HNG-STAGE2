from django.core.management.base import BaseCommand
import json
from core.models import Profile

class Command(BaseCommand):
    help = "Import data from a JSON file into the Profile model"
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to import')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        try:
            with open(json_file_path, 'r') as json_file:
                raw_data = json.load(json_file)
                data = raw_data.get('profiles', [])
                profiles_to_create = []
            
                for item in data:
                    name = item.get('name')
                    if name and not Profile.objects.filter(name=name).exists():
                        profiles_to_create.append(
                            Profile(
                                name = item.get('name'),
                                gender = item.get('gender'),
                                gender_probability = item.get('gender_probability'),
                                age = item.get('age'),
                                age_group = item.get('age_group'),
                                country_id = item.get('country_id'),
                                country_name = item.get('country_name'),
                                country_probability = item.get('country_probability'),
                                )
                            )
                     
                Profile.objects.bulk_create(profiles_to_create)

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully imported {len(profiles_to_create)} profiles from {json_file_path}')
                    )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file_path}')
                )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON format in file: {json_file_path}')
                )    