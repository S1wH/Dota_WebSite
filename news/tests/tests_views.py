from django.test import TestCase
from news.models import News
from mixer.backend.django import mixer
from users.models import MyUser


class TestViews(TestCase):

    def test_str(self):
        response = self.client.get('/news/list/')
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        response = self.client.get('/news/list/')
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 0)

        news = mixer.blend(News, header='123', importance_index=True)

        response = self.client.get('/news/list/')
        self.assertEqual(len(response.context['object_list']), 1)

        response = self.client.get('/news/list/')
        self.assertEqual(response.context['object_list'][0].header, news.header)

        # some text
        self.assertEqual(response.context['some text'], 'some text example')

    def test_content(self):
        response = self.client.get('/news/list/')

        # print(response.content)
        # print(type(response.content))

        button_create = '<a class="btn btn-primary" href="/news/create/">Создать</a>'

        self.assertIn(button_create.encode(encoding='utf-8'), response.content)
        self.assertIn(button_create, response.content.decode(encoding='utf-8'))

    def test_permissions_detail_view(self):
        news = mixer.blend(News, header='123')
        url = f'/news/detail/{news.pk}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        username = 'fred'
        password = 'secret'
        MyUser.objects.create_user(username, 'fred@fred.com', password)

        self.client.login(username=username, password=password)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        url = '/news/create/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


        # self.client.logout()

