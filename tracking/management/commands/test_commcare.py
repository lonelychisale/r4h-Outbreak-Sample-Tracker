from django.core.management.base import BaseCommand
from tracking.services.commcare import fetch_cases


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        data = fetch_cases()
        import json

        print(json.dumps(data["meta"], indent=4))
        fields = set()

        for case in data["objects"]:

            properties = case.get("properties", {})

            for field in properties.keys():
                fields.add(field)

        print("\nFIELDS FOUND\n")

        for field in sorted(fields):
            print(field)