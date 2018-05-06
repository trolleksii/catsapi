from django.shortcuts import reverse
from django.test import TestCase


class TestUIViews(TestCase):

    def test_indexview_template(self):
        response = self.client.get(
            reverse('ui:index_page'),
        )
        self.assertTemplateUsed(response, 'index.html')

    def test_breedsview_template(self):
        response = self.client.get(
            reverse('ui:breeds_page'),
        )
        self.assertTemplateUsed(response, 'breeds.html')

    def test_specsview_template(self):
        response = self.client.get(
            reverse('ui:specs_page'),
        )
        self.assertTemplateUsed(response, 'specs.html')
