import re

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils import translation

from apps.core.testing.mixins import TestModelStringMixin

from .factories import *


class ProfileTests(TestModelStringMixin, TestCase):

    def setUp(self):
        translation.activate('en')
        AdditionalTextFieldFactory()
        AdditionalTextareaFieldFactory()
        self.instance = UserFactory()

    def test_get_profile_update(self):
        """
        An authorized GET request to the profile update form returns the form.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_profile_update_redirect(self):
        """
        An unauthorized GET request to the profile update form gets
        redirected to login.
        """
        url = reverse('profile_update')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('account_login') + '?next=' + url)

    def test_post_profile_update(self):
        """
        An authorized POST request to the profile update form updates the
        user and redirects to home.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'text': 'text',
            'textarea': 'textarea',
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_post_profile_update_cancel(self):
        """
        An authorized POST request to the profile update form updates with
        cancel redirects to home.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'cancel': 'cancel'
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)

    def test_post_profile_update_cancel2(self):
        """
        An authorized POST request to the profile update form updates with
        cancel and the next field redirects to the given url.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'cancel': 'cancel',
            'next': reverse('account_change_password')
        })
        self.assertRedirects(response, reverse('account_change_password'))

    def test_post_profile_update_next(self):
        """
        An authorized POST request to the profile update form with next field
        updates the user and redirects to the given url.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'text': 'text',
            'textarea': 'textarea',
            'next': reverse('account_change_password')
        })
        self.assertRedirects(response, reverse('account_change_password'))

    def test_post_profile_update_next2(self):
        """
        An authorized POST request to the profile update form with next
        field set to profile_update updates the user and redirects to home.
        """
        self.client.login(username='user', password='user')

        url = reverse('profile_update')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Albert',
            'last_name': 'Admin',
            'text': 'text',
            'textarea': 'textarea',
            'next': reverse('profile_update')
        })
        self.assertRedirects(response, reverse('home'), target_status_code=302)


class AdditionalFieldTests(TestModelStringMixin, TestCase):

    def setUp(self):
        translation.activate('en')
        self.instance = AdditionalTextFieldFactory()


class PasswordTests(TestCase):

    def setUp(self):
        UserFactory()

        translation.activate('en')

    def test_password_change_get(self):
        """
        An authorized GET request to the password change form returns the form.
        """
        self.client.login(username='user', password='user')

        url = reverse('account_change_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_change_post(self):
        """
        An authorized POST request to the password change form updates the
        password and redirects to home.
        """
        self.client.login(username='user', password='user')

        url = reverse('account_change_password')
        response = self.client.post(url, {
            'old_password': 'user',
            'new_password1': 'resu',
            'new_password2': 'resu',
        })
        self.assertEqual(response.status_code, 200)

    def test_password_reset_get(self):
        """
        A GET request to the password reset form returns the form.
        """
        url = reverse('account_reset_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_post_invalid(self):
        """
        A POST request to the password reset form with an invalid mail address
        sends no mail.
        """
        url = reverse('account_reset_password')
        response = self.client.post(url, {'email': 'wrong@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_post_valid(self):
        """
        A POST request to the password reset form with an invalid mail address
        sends a mail with a correct link.
        """
        url = reverse('account_reset_password')
        response = self.client.post(url, {'email': 'user@example.com'})
        self.assertRedirects(response, reverse('account_reset_password_done'))
        self.assertEqual(len(mail.outbox), 1)

        # get the link from the mail
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[0].body)
        self.assertEqual(len(urls), 1)

        # get the password_reset page
        response = self.client.get(urls[0])
        self.assertEqual(response.status_code, 200)
