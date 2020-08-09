import os
from django.core.management.base import BaseCommand
from django.conf import settings

# pylint: disable=import-error,no-name-in-module
from main.tests.helpers.orthanc_rest_handler import OrthancRestHandler


class Command(BaseCommand):
    help = "Clear both Orthanc instances and upload DICOM files to Orthanc 1 instance."

    def handle(self, *args, **options):
        dicoms_folder = settings.BASE_DIR / "samples" / "dicoms"
        orthanc1_host = os.environ.get("ORTHANC1_HOST")
        if not orthanc1_host:
            orthanc1_host = "localhost"
        handler = OrthancRestHandler(host=orthanc1_host, port=6501)
        handler.clear()
        handler.upload_files(dicoms_folder)

        orthanc2_host = os.environ.get("ORTHANC2_HOST")
        if not orthanc2_host:
            orthanc1_host = "localhost"
        handler = OrthancRestHandler(host=orthanc2_host, port=6502)
        handler.clear()
