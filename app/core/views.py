from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIClient
from rest_framework.viewsets import GenericViewSet

from core.models import CampingTag
from camping.serializers import TagSerialzier

