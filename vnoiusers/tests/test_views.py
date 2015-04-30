# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse

from django.test import TestCase
from django.test import Client
import mock
from vnoiusers import views as user_views


class UserViewTest(TestCase):

    fixtures = ['test_auth.json', 'test_vnoiusers.json']

    def setUp(self):
        self.client = Client()
        self.user_admin = User.objects.get(username='admin')
        self.user_vnoi = User.objects.get(username='vnoiuser')
        self.user_vnoi2 = User.objects.get(username='vnoiuser2')

        self.passwords = {
            'admin': 'admin',
            'vnoiuser': 'vnoiuser',
            'vnoiuser2': 'vnoiuser'
        }

    def test_url_resolve(self):
        # profile
        resolver = resolve('/user/1/')
        self.assertEqual(resolver.view_name, 'user:profile')
        self.assertEqual(resolver.func, user_views.user_profile)

        # login
        resolver = resolve('/user/login')
        self.assertEqual(resolver.view_name, 'user:login')
        self.assertEqual(resolver.func, user_views.user_login)

        # register
        resolver = resolve('/user/register')
        self.assertEqual(resolver.view_name, 'user:register')

        # link CF account
        resolver = resolve('/user/link_codeforces')
        self.assertEqual(resolver.view_name, 'user:link_codeforces')
        self.assertEqual(resolver.func, user_views.link_codeforces_account)

        # unlink CF account
        resolver = resolve('/user/unlink_codeforces')
        self.assertEqual(resolver.view_name, 'user:unlink_codeforces')
        self.assertEqual(resolver.func, user_views.unlink_codeforces_account)

        # link VOJ account
        resolver = resolve('/user/link_voj')
        self.assertEqual(resolver.view_name, 'user:link_voj')
        self.assertEqual(resolver.func, user_views.link_voj_account)

        # unlink VOJ account
        resolver = resolve('/user/unlink_voj')
        self.assertEqual(resolver.view_name, 'user:unlink_voj')
        self.assertEqual(resolver.func, user_views.unlink_voj_account)

        # add friend
        resolver = resolve('/user/add_friend/1')
        self.assertEqual(resolver.view_name, 'user:add_friend')
        self.assertEqual(resolver.func, user_views.add_friend)

        # remove friend
        resolver = resolve('/user/remove_friend/1')
        self.assertEqual(resolver.view_name, 'user:remove_friend')
        self.assertEqual(resolver.func, user_views.remove_friend)

    def test_load_profile(self):
        # Invalid profiles
        response = self.client.get(reverse('user:profile', kwargs={'username': 999}))
        self.assertEqual(response.status_code, 404)

        # Note: since reverse will fail when user ID is not an integer, we must hard code the URL here
        self.assertEqual(response.status_code, 404)

        # Not logged in - load profiles
        # Admin profile
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_admin.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].id, self.user_admin.id)
        self.assertFalse(response.context['is_friend'])

        # Load vnoiuser profile
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].id, self.user_vnoi.id)
        self.assertFalse(response.context['is_friend'])

        # Login as admin
        self.login(self.user_admin)

        # Admin profile
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_admin.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].id, self.user_admin.id)
        # Cannot be friend with himself
        self.assertFalse(response.context['is_friend'])

        # Load vnoiuser profile
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].id, self.user_vnoi.id)
        self.assertTrue(response.context['is_friend'])

        # Load a friend profile
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].id, self.user_vnoi2.id)
        self.assertFalse(response.context['is_friend'])

    def test_login(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

        # Login and try again
        self.login(self.user_vnoi)
        response = self.client.get(reverse('user:login'), follow=True)
        # Since we already logged in before, views should redirect
        self.assertRedirects(response, reverse('main:index'))
        self.client.logout()

        # Now try to submit form

        # Login with wrong password
        response = self.client.post('/user/login?next=/message/inbox/', {
            'username': self.user_vnoi.username,
            'password': 'obviously_wrong_password'
        })
        self.assertEqual(response.status_code, 200)

        # Login success
        response = self.client.post('/user/login?next=/message/inbox/', {
            'username': self.user_vnoi.username,
            'password': self.passwords[self.user_vnoi.username]
        })
        self.assertRedirects(response, '/message/inbox/')

    def test_logout(self):
        # Try logout before logging in
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, '/user/login?next=/user/logout')

        # Now, we login
        self.login(self.user_vnoi)
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

        # Try logout again
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, '/user/login?next=/user/logout')

    def test_register(self):
        # Load register page
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

        # Login & load register page --> redirects to /
        self.login(self.user_vnoi)
        response = self.client.get(reverse('user:register'))
        self.assertRedirects(response, reverse('main:index'))

        # Now register a new user
        self.client.logout()
        response = self.client.post(reverse('user:register'), {
            'username': 'RR',
            'password1': '12345',
            'password2': '12345',
            'first_name': 'Trung',
            'last_name': 'Nguyen',
            'dob': '1992-06-23',
            'email': 'test@gmail.com'
        })
        self.assertEqual(response.status_code, 200)

        # Query DB to get activation code for this account
        user = User.objects.get(username='RR')
        self.assertIsNotNone(user)
        activation_key = user.profile.activation_key

        # Activate the account!
        response = self.client.post(reverse('user:register_confirm', kwargs={
            'activation_key': activation_key
        }))
        self.assertRedirects(response, reverse('user:login'))

        # Check that we can actually login
        self.assertTrue(self.client.login(username='RR', password='12345'))

        # Now try to go to account activation link again, it should redirects to /
        response = self.client.post(reverse('user:register_confirm', kwargs={
            'activation_key': activation_key
        }), follow=True)
        self.assertRedirects(response, reverse('main:index'))

    def test_link_codeforces(self):
        self.login(self.user_vnoi)

        # User should be able to go to link CF
        response = self.client.get(reverse('user:link_codeforces'))
        self.assertEqual(response.status_code, 200)

        # User should not be able to go to unlink CF (since he has not linked his account)
        response = self.client.get(reverse('user:unlink_codeforces'))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Link CF account and try again
        self.user_vnoi.profile.codeforces_account = 'abc'
        self.user_vnoi.profile.save()

        # Verify that the CF account is there
        tmp = User.objects.get(username='vnoiuser')
        self.assertEqual(tmp.profile.codeforces_account, 'abc')

        # Unlink CF account!
        response = self.client.get(reverse('user:unlink_codeforces'))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Verify again that the CF account is gone
        tmp = User.objects.get(username='vnoiuser')
        self.assertEqual(tmp.profile.codeforces_account, '')

    @mock.patch('vnoiusers.forms.CodeforcesLinkForm.is_valid')
    def test_link_codeforces_submit(self, mock_is_valid):
        # First, login to use link CF function
        self.login(self.user_vnoi)

        # Mock the form check to return True --> link account success
        mock_is_valid.return_value = True
        response = self.client.post(reverse('user:link_codeforces'), {'username': 'RR', 'password': '12345'})
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Logout & use different account
        self.client.logout()
        self.login(self.user_vnoi2)
        # Mock the form validation check to return False --> link account fail
        mock_is_valid.return_value = False
        response = self.client.post(reverse('user:link_codeforces'), {'username': 'RR2', 'password': '12345'})
        # Here we should see the form again
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('message', response.context)

    def test_link_voj(self):
        self.login(self.user_vnoi)

        # User should be able to go to link VOJ account page
        response = self.client.get(reverse('user:link_voj'))
        self.assertEqual(response.status_code, 200)

        # User cannot go to unlink VOJ because he has not linked VOJ account
        response = self.client.get(reverse('user:unlink_voj'))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Link VOJ account and try again
        self.user_vnoi.profile.voj_account = 'abc'
        self.user_vnoi.profile.save()

        # Verify that the VOJ account is there
        tmp = User.objects.get(username='vnoiuser')
        self.assertEqual(tmp.profile.voj_account, 'abc')

        # Unlink VOJ account!
        response = self.client.get(reverse('user:unlink_voj'))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Verify again that the VOJ account is gone
        tmp = User.objects.get(username='vnoiuser')
        self.assertEqual(tmp.profile.voj_account, '')

    @mock.patch('vnoiusers.forms.VojLinkForm.is_valid')
    def test_link_voj_submit(self, mock_is_valid):
        # First, login to use link VOJ function
        self.login(self.user_vnoi)

        # Mock form valid check to True
        mock_is_valid.return_value = True
        response = self.client.post(reverse('user:link_voj'), {'username': 'RR', 'password': '12345'})
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.id}))

        # Logout & use different account
        self.client.logout()
        self.login(self.user_vnoi2)

        # Mock the form valid check to False
        mock_is_valid.return_value = False
        response = self.client.post(reverse('user:link_voj'), {'username': 'RR2', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('message', response.context)

    def test_list_friend(self):
        self.login(self.user_admin)
        response = self.client.get(reverse('user:friend_list'))
        self.assertEqual(response.status_code, 200)

    def test_unfriend(self):
        self.login(self.user_admin)

        # Load vnoiuser account to verify that we are currently friend
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_friend'])

        # Unfriend!
        response = self.client.get(reverse('user:remove_friend', kwargs={'username': self.user_vnoi.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.username}))

        # Verify that we are no longer friends
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.username}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_friend'])

        # Unfriend again (this should not have any effect)
        response = self.client.get(reverse('user:remove_friend', kwargs={'username': self.user_vnoi.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.username}))

        # Verify that we are still not friends
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.username}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_friend'])

    def test_add_friend(self):
        self.login(self.user_admin)

        # Load vnoiuser2 account to verify that we are currently friend
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi2.username}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_friend'])

        # Add friend!
        response = self.client.get(reverse('user:add_friend', kwargs={'username': self.user_vnoi2.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi2.username}))

        # Verify that we are no longer friends
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi2.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_friend'])

        # Add friend again (this should not have any effect)
        response = self.client.get(reverse('user:add_friend', kwargs={'username': self.user_vnoi2.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi2.username}))

        # Verify that we are still not friends
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi2.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_friend'])

    def test_add_friend_self(self):
        self.login(self.user_vnoi)

        response = self.client.get(reverse('user:add_friend', kwargs={'username': self.user_vnoi.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.username}))

        # Verify not friend
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.username}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_friend'])

        # Also test for remove friend
        response = self.client.get(reverse('user:remove_friend', kwargs={'username': self.user_vnoi.username}))
        self.assertRedirects(response, reverse('user:profile', kwargs={'username': self.user_vnoi.username}))

        # Verify not friend
        response = self.client.get(reverse('user:profile', kwargs={'username': self.user_vnoi.username}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['is_friend'])

    def test_list_users(self):
        # User who is not logged in should be able to search for user
        response = self.client.get(reverse('user:index'))
        self.assertRedirects(response, '/user/login?next=/user/index')

        # Login and try again
        self.login(self.user_admin)

        # Test get (load user search form)
        response = self.client.get(reverse('user:index'))
        self.assertEqual(response.status_code, 200)

        # Search for prefix vnoi
        response = self.client.post(reverse('user:index'), {'user_prefix': 'vnoi'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['users'], [
            repr(self.user_vnoi),
            repr(self.user_vnoi2)
        ], ordered=False)

        # Search for prefix 'a'
        response = self.client.post(reverse('user:index'), {'user_prefix': 'a'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['users'], [
            repr(self.user_admin)
        ], ordered=False)

        # Search for prefix 'abcxyz123' (should return no result)
        response = self.client.post(reverse('user:index'), {'user_prefix': 'abcxyz123'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['users'], [], ordered=False)

    def login(self, account):
        self.assertTrue(self.client.login(username=account.username, password=self.passwords[account.username]))
