from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import Group
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from adit.accounts.factories import UserFactory
from adit.main.factories import DicomServerFactory
from ..models import BatchTransferJob

csv_data = b"""\
RowKey;PatientID;PatientName;PatientBirthDate;StudyDate;Modality;Pseudonym;Exclude
1;10007;Papaya, Pamela;29.08.1976;19.08.2018;MR;ABU5QZL9;
2;10002;Banana, Ben;18.02.1962;27.03.2018;CT;DEDH6SVQ;
3;10002;Banana, Ben;18.02.1962;15.09.2019;MR;DEDH6SVQ;
"""

# Somehow the form data must be always generated from scratch (maybe cause of the
# SimpleUploadedFile) otherwise tests fail.
def create_form_data():
    return {
        "source": DicomServerFactory().id,
        "destination": DicomServerFactory().id,
        "project_name": "Apollo project",
        "project_description": "Fly to the moon",
        "csv_file": SimpleUploadedFile(
            name="sample_sheet.csv", content=csv_data, content_type="text/csv"
        ),
    }


class BatchTransferJobCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup test users
        cls.user_without_permission = UserFactory()

        cls.user_with_permission = UserFactory()
        batch_transferrers_group = Group.objects.get(name="batch_transferrers")
        cls.user_with_permission.groups.add(batch_transferrers_group)

    def test_user_must_be_logged_in_to_access_view(self):
        response = self.client.get(reverse("batch_transfer_job_create"))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse("batch_transfer_job_create"))
        self.assertEqual(response.status_code, 302)

    def test_user_must_have_permission_to_access_view(self):
        self.client.force_login(self.user_without_permission)
        response = self.client.get(reverse("batch_transfer_job_create"))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse("batch_transfer_job_create"))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_with_permission_can_access_form(self):
        self.client.force_login(self.user_with_permission)
        response = self.client.get(reverse("batch_transfer_job_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "batch_transfer/batch_transfer_job_form.html")

    @patch("adit.batch_transfer.tasks.batch_transfer.delay")
    def test_batch_job_created_and_enqueued_with_auto_verify(
        self, batch_transfer_delay_mock
    ):
        self.client.force_login(self.user_with_permission)
        with self.settings(BATCH_AUTO_VERIFY=True):
            self.client.post(reverse("batch_transfer_job_create"), create_form_data())
            job = BatchTransferJob.objects.first()
            self.assertEqual(job.requests.count(), 3)
            batch_transfer_delay_mock.assert_called_once_with(job.id)

    @patch("adit.batch_transfer.tasks.batch_transfer.delay")
    def test_batch_job_created_and_not_enqueued_without_auto_verify(
        self, batch_transfer_delay_mock
    ):
        self.client.force_login(self.user_with_permission)
        with self.settings(BATCH_AUTO_VERIFY=False):
            self.client.post(reverse("batch_transfer_job_create"), create_form_data())
            job = BatchTransferJob.objects.first()
            self.assertEqual(job.requests.count(), 3)
            batch_transfer_delay_mock.assert_not_called()

    def test_job_cant_be_created_with_missing_fields(self):
        self.client.force_login(self.user_with_permission)
        for key_to_exclude in create_form_data():
            invalid_form_data = create_form_data().copy()
            del invalid_form_data[key_to_exclude]
            response = self.client.post(
                reverse("batch_transfer_job_create"), invalid_form_data
            )
            self.assertGreater(len(response.context["form"].errors), 0)
            self.assertIsNone(BatchTransferJob.objects.first())