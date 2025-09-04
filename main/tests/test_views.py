from django.test import TestCase
from django.urls import reverse

class IndexViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, 'Главная')
        self.assertIn('test_top_products', response.context)
        self.assertEqual(len(response.context['test_top_products']), 4)

class AboutViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'О магазине')

class ProjectViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('main:project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/project.html')
        self.assertContains(response, 'О проекте')

