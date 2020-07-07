from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()


class TestProfileAndPosts(TestCase):

    def setUp(self):
        self.text = 'Тестовое сообщение'

        self.logged_client = Client()
        self.client = Client()

        self.user = User.objects.create_user(
            username='TestUser', email='Test@test.com',
            password='DhfidhgdTSfs467')

        self.group = Group.objects.create(
            title='test_group',
            slug='test_group'
        )

        self.logged_client.force_login(self.user)

    def test_profile_created(self):
        profile_url = reverse('profile', kwargs={'username': self.user})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile.html')

    def test_unauthorized_redirect(self):
        self.client.post(reverse('new-post'), follow=True)
        login_url = self.client.post(reverse('login'))
        self.assertTemplateUsed(login_url,
                                template_name='registration/login.html')

    def test_post(self):
        post_test = self.logged_client.post(
            reverse('new-post'), {'text': self.text, 'group': self.group.id},
            follow=True)
        group_url = self.logged_client.get(
            reverse('group', kwargs={'slug': self.group.slug}))
        self.assertContains(group_url, text=self.text, count=1,
                            status_code=200)
        self.assertEqual(post_test.status_code, 200)
        self.assertEqual(1, Post.objects.count())
        created_post = Post.objects.get(text=self.text)
        self.assertEqual(self.text, created_post.text)

    def check_contain_post(self, url, text, group=None, user=None):
        self.assertContains(url, text=text, count=1, status_code=200)

    def test_post_view(self):
        self.logged_client.post(
            reverse('new-post'), {'text': self.text, 'group': self.group.id},
            follow=True)
        post = Post.objects.get(text=self.text)
        url_list = [
            self.logged_client.get(reverse('index')),
            self.logged_client.get(
                reverse('profile', kwargs={'username': self.user})),
            self.logged_client.get(
                reverse('group', kwargs={'slug': self.group.slug})),
            self.logged_client.get(reverse('post', kwargs={
                'username': self.user,
                'post_id': post.id}))
        ]
        for url in url_list:
            with self.subTest(url=url):
                self.check_contain_post(url, text=self.text, group=self.group,
                                        user=self.user)

    def test_post_edit(self):
        post = Post.objects.create(text=self.text, author=self.user)
        new_text = 'Измененное сообщение'
        self.logged_client.post(
            reverse('post_edit', kwargs={
                'username': self.user,
                'post_id': post.id
            }),
            {'text': new_text, 'group': self.group.id}
        )
        url_list = [
            self.logged_client.get(reverse('index')),
            self.logged_client.get(
                reverse('profile', kwargs={'username': self.user})),
            self.logged_client.get(
                reverse('group', kwargs={'slug': self.group.slug})),
            self.logged_client.get(reverse('post', kwargs={
                'username': self.user,
                'post_id': post.id}))
        ]
        for url in url_list:
            with self.subTest(url=url):
                self.check_contain_post(url, text=new_text, group=self.group,
                                        user=self.user)
