from django.test import TestCase
from items.models import Sport, ItemCondition, Item
from members.models import Profile
from django.contrib.auth.models import User

class SportModelTest(TestCase):
    def test_sport_creation(self):
        sport = Sport.objects.create(name="Football")
        self.assertEqual(str(sport), "Football")

    def test_sport_ordering(self):
        Sport.objects.create(name="Basketball")
        Sport.objects.create(name="Tennis")
        sports = Sport.objects.all()
        self.assertEqual(list(sports.values_list('name', flat=True)), ["Basketball", "Tennis"])

class ItemConditionModelTest(TestCase):
    def test_item_condition_creation(self):
        condition = ItemCondition.objects.create(name="New")
        self.assertEqual(str(condition), "New")

    def test_item_condition_ordering(self):
        ItemCondition.objects.create(name="Used")
        ItemCondition.objects.create(name="New")
        conditions = ItemCondition.objects.all()
        self.assertEqual(list(conditions.values_list('name', flat=True)), ["New", "Used"])

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)
        self.sport = Sport.objects.create(name="Running")
        self.condition = ItemCondition.objects.create(name="Like New")

    def test_item_creation(self):
        item = Item.objects.create(
            name="Running Shoes",
            sport=self.sport,
            advertiser=self.profile,
            price=99.99,
            condition=self.condition,
        )
        self.assertEqual(str(item), "Running Shoes")
        self.assertFalse(item.sold)
