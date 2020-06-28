from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post

User = get_user_model()


class TestProfileAndPosts(TestCase):

    def setUp(self):
        self.logged_client = Client()
        self.client = Client()

        self.user = User.objects.create_user(
            username='UserForTest', email='Test@test.ru',
            password='AsefdasDSa32')

        self.text = 'Тестовое сообщение'

        self.logged_client.force_login(self.user)

    def test_profile_created(self):
        profile_url = reverse('profile',
                              kwargs={
                                  'username': self.user})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile.html')

    def test_unauthorized_redirect(self):
        self.client.post(reverse('new-post'), follow=True)
        login_url = self.client.post(reverse('login'))
        self.assertTemplateUsed(login_url,
                                template_name='registration/login.html')

    def test_post(self):
        post_test = self.logged_client.post(reverse('new-post'),
                                            {'text': self.text}, follow=True)
        self.assertEqual(post_test.status_code, 200)
        self.assertEqual(1, Post.objects.count())
        created_post = Post.objects.get(text=self.text)
        self.assertIn(self.text, created_post.text)

    def test_post_view(self):
        self.logged_client.post(reverse('new-post'), {'text': self.text})
        post = Post.objects.get(text=self.text)
        index_url = self.logged_client.get(reverse('index'))
        profile_url = self.logged_client.get(
            reverse('profile', kwargs={'username': self.user}))
        post_url = self.logged_client.get(reverse('post',
                                                  kwargs={
                                                      'username': self.user,
                                                      'post_id': post.id}))
        self.assertContains(index_url, text=self.text, count=1,
                            status_code=200)
        self.assertContains(profile_url, text=self.text, count=1,
                            status_code=200)
        self.assertContains(post_url, text=self.text, count=1,
                            status_code=200)

    def test_post_edit(self):
        post = Post.objects.create(text=self.text,
                                   author=self.user)
        new_text = 'А теперь это сообщение поменялось'
        self.logged_client.post(reverse('post_edit',
                                        kwargs={'username': self.user,
                                                'post_id': post.id}),
                                {'text': new_text})
        index_url = self.logged_client.get(reverse('index'))
        profile_url = self.logged_client.get(
            reverse('profile', kwargs={'username': self.user}))
        post_url = self.logged_client.get(reverse('post',
                                                  kwargs={
                                                      'username': self.user,
                                                      'post_id': post.id}))
        self.assertContains(index_url, text=new_text, count=1,
                            status_code=200)
        self.assertContains(profile_url, text=new_text, count=1,
                            status_code=200)
        self.assertContains(post_url, text=new_text, count=1,
                            status_code=200)
