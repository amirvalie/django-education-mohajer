from django.test import TestCase
from .models import Contact
from extensions.utils import jalali_converter

# Create your tests here.


class TestOrderModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contact.objects.create(
            name="Amir",
            email="amir@gmail.com",
            phone_number="090332895704",
            subject="test",
            message="test",
        )

    def setUp(self) -> None:
        self.contact = Contact.objects.get(id=1)

    def test_jalali_convertor(self):
        jalali_time = self.contact.jalali_time()
        self.assertEqual(jalali_time, jalali_converter(self.contact.create_time))

    def test_email_label(self):
        email_label = self.contact._meta.get_field("email").verbose_name
        self.assertEqual(email_label, "ایمیل")

    def test_name_label(self):
        name_label = self.contact._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "نام")

    def test_phone_number_label(self):
        phone_number_label = self.contact._meta.get_field("phone_number").verbose_name
        self.assertEqual(phone_number_label, "شماره تماس")
