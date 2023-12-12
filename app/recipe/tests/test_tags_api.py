"""Test for tags"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe

from recipe.serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")


def create_user(email="test@example.com", passwrod="pas123"):
    return get_user_model().objects.create_user(email, passwrod)


def detail_url(tag_id):  # create a unique url for a specific tag detail
    return reverse("recipe:tag-detail", args=[tag_id])


class PublicTagsApiTest(TestCase):
    """unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retriving tags"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test auth API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tag(self):
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email="user2@example.com")
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort food")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        tag = Tag.objects.create(user=self.user, name="After Dinner")
        payload = {"name": "Dessert"}

        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload["name"])
    
    def test_delete_tag(self):
        tag = Tag.objects.create(user=self.user, name="Comfort food") 
        
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
    
    def test_filter_tags_assigned_to_recipe(self):
        """Test listing tags by those assignened to recipes"""
        tag1 = Tag.objects.create(user=self.user, name="thai")
        tag2 = Tag.objects.create(user=self.user, name="italian")

        recipe = Recipe.objects.create(
            title="Some recipe",
            time_minutes=5,
            price=Decimal("40.00"),
            user=self.user,
        )

        recipe.tags.add(tag1)

        # filter by tags that are assignend to a recipe
        res = self.client.get(TAG_URL, {"assigned_only": 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_fitered_tagss_unique(self):
        """Test filtered tagss returns a unique list"""
        tag1 = Tag.objects.create(user=self.user, name="tag1")
        tag2 = Tag.objects.create(user=self.user, name="tag2")
        recipe1 = Recipe.objects.create(
            title="Some recipe",
            time_minutes=5,
            price=Decimal("40.00"),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title="egs",
            time_minutes=5,
            price=Decimal("40.00"),
            user=self.user,
        )
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag1)

        res = self.client.get(TAG_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
