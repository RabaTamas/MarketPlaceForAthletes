from django.test import Client, TestCase

# Create your tests here.

from django.contrib.auth.models import User
from members.models import Profile, Score
from django.urls import reverse
from items.models import Sport, Item, ItemCondition
from members.forms import CreateListingForm

# Models test 
class ProfileModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = Profile.objects.create(user=self.user, bio="Test bio")
    
    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), self.user.get_short_name())

    def test_profile_get_items_no_items(self):
        self.assertEqual(self.profile.get_items(), "No items")

class ScoreModelTest(TestCase):
    def setUp(self):
        self.rater = User.objects.create_user(username="rater", password="password123")
        self.rated = User.objects.create_user(username="rated", password="password123")
        self.score = Score.objects.create(rater_user=self.rater, rated_user=self.rated, score=5)
    
    def test_score_str_representation(self):
        self.assertEqual(
            str(self.score), 
            f'{self.rater} rated {self.rated} with {self.score.score}'
        )

    def test_score_unique_constraint(self):
        with self.assertRaises(Exception):
            Score.objects.create(rater_user=self.rater, rated_user=self.rated, score=4)


# Views Test
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = Profile.objects.create(user = self.user)
        # self.profile.user_id = self.user.pk
    
    def test_login_successful(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))
    
    def test_login_unsuccessful(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

class SignupUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_signup_success(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "password123",
            "password2": "password123",
            "first_name": "John",
            "last_name": "Doe",
        })
        # self.assertTemplateUsed(response, "home.html")
        self.assertEqual(response.status_code, 200)

    def test_signup_failure(self):
        response = self.client.post(reverse("signup"), {
            "username": "",
            "password1": "password123",
            "password2": "password123",
        })
        self.assertContains(response, "An error happened!")

class HomeViewTest(TestCase):
     def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.sport = Sport.objects.create(name="Football")
        self.condition = ItemCondition.objects.create(name="New")
        self.item = Item.objects.create(
            name="Football Shoes",
            sport=self.sport,
            advertiser=Profile.objects.create(user=self.user),
            price=50.0,
            condition=self.condition,
            sold = False
        )

     def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Football Shoes")

     def test_home_view_search(self):
        response = self.client.get(reverse("home"), {"search": "Football"})
        self.assertContains(response, "Football Shoes")

     def test_home_filters(self):
        response = self.client.get(reverse('home'), {
            'sports': [self.sport.id],
            'conditions': [self.condition.id],
            'min_price': 30,
            'max_price': 60
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

     def test_home_sorting(self):
        response = self.client.get(reverse('home'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

class LogoutUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_logout_user(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

class ItemViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)
        self.sport = Sport.objects.create(name="Basketball")
        self.item = Item.objects.create(
            name="Basketball",
            sport=self.sport,
            advertiser=self.profile,
            price=25.0,
            condition=ItemCondition.objects.create(name="Used"),
            sold=False
        )

    def test_item_view(self):
        response = self.client.get(reverse('item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

class CreateListingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)
        self.sport = Sport.objects.create(name="Tennis")
        self.condition = ItemCondition.objects.create(name="Good")
        self.client.login(username="testuser", password="12345")

    def test_create_listing_success(self):
         response = self.client.post(reverse('addlisting'),{
             'name' : "Tennis Racket",
             'sport' : self.sport.id,
             'price': 100,
             'condition' : self.condition.id,
             'description': 'asd'

             })
         self.assertEqual(response.status_code, 302)
         self.assertTrue(Item.objects.filter(name="Tennis Racket").first() != None)

class MyAdsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user)
        self.item = Item.objects.create(
            name="Golf Club",
            sport=Sport.objects.create(name="Golf"),
            advertiser=self.profile,
            price=150.0,
            condition=ItemCondition.objects.create(name="New"),
        )
        self.client.login(username="testuser", password="12345")

    def test_my_ads(self):
        response = self.client.get(reverse('my_ads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_delete_item(self):
        response = self.client.post(reverse('my_ads'), {'item_ids': [self.item.id]})
        self.assertRedirects(response, reverse('my_ads'))
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

class EditItemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user)
        self.sport = Sport.objects.create(name='Football')
        self.condition = ItemCondition.objects.create(name='New')
        self.item = Item.objects.create(
            name='Football Ball',
            sport=self.sport,
            advertiser=self.profile,
            price=20,
            condition=self.condition
        )
        self.url = reverse('edit_item', args=[self.item.id])

    def test_edit_item_success(self):
        self.client.login(username='testuser', password='password')
        data = {
            'name': 'Updated Football Ball',
            'price': 25,
            'sport': self.sport.id,
            'condition': self.condition.id,
            'description':'asd',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Football Ball')
        self.assertEqual(self.item.price, 25)

class MyProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user, bio='Old Bio')
        self.url = reverse('my_profile')

    def test_update_profile_success(self):
        self.client.login(username='testuser', password='password')
        data = {
            'first_name': 'Updated Name',
            'last_name':'Updated LastName',
            'username':'testuser',
            'bio': 'New Bio',
            'email':'testuser@gmail.com',
            'password':'12345'
        }
        response = self.client.post(self.url, data)
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertEqual(self.profile.bio, 'New Bio')

class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword')
        self.url = reverse('change_password')

    def test_change_password_success(self):
        self.client.login(username='testuser', password='oldpassword')
        data = {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

class AdvertisersViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.profile1 = Profile.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.profile2 = Profile.objects.create(user=self.user2)
        self.url = reverse('advertisers')

    def test_advertisers_search(self):
        response = self.client.get(self.url, {'search': 'user1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertNotContains(response, 'user2')

class AddScoreViewTest(TestCase):
    def setUp(self):
        self.rater = User.objects.create_user(username='rater', password='password')
        self.rated = User.objects.create_user(username='rated', password='password')
        self.url = reverse('add_score', args=[self.rated.id])

    def test_add_score_success(self):
        self.client.login(username='rater', password='password')
        data = {'score': 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Score.objects.filter(rater_user=self.rater, rated_user=self.rated, score=5).exists())
