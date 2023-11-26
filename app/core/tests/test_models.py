"""
Tests for models
"""
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="pass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_user_with_email(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_email = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag 1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name="ingredient1",
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path, create the path using uuid as a unique identifier"""
        uuid = "test_uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
