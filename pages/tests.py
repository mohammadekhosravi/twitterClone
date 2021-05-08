from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import HomePageView, AboutPageView, HomeRedirectView


class HomeRedirectTests(TestCase):

    def setUp(self):
        self.client.force_login(get_user_model().objects.get_or_create(username='testuser')[0])
        url = reverse('home_redirect')
        self.response = self.client.get(url, follow=True)

    def test_root_url_redirects_to_homepage_view(self):
        expected_url = reverse('home')
        self.assertRedirects(self.response, expected_url=expected_url, status_code=301, target_status_code=200)

    def test_homeredirect_url_resolves_homeredirectview(self):
        view = resolve(reverse('home_redirect'))
        self.assertEqual(
            view.func.__name__,
            HomeRedirectView.as_view().__name__
        )


class HomePageTests(TestCase):

    def setUp(self):
        self.client.force_login(get_user_model().objects.get_or_create(username='testuser')[0])
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    # def test_homepage_contains_correct_html(self):
    #     self.assertContains(self.response, 'TWITTER')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve(reverse('home'))
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )


class AboutPageTests(TestCase):

    def setUp(self):
        self.client.force_login(get_user_model().objects.get_or_create(username='testuser')[0])
        url = reverse('about')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Mohammad Khosravi')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve(reverse('about'))
        self.assertEqual(
            view.func.__name__,
            AboutPageView.as_view().__name__
        )
