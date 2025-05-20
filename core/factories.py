import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from blog.models import BlogPost


class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.Sequence(lambda n: f'Blog post title {n}')
    content = factory.Faker('paragraph', nb_sentences=5)
    created_at = factory.LazyFunction(timezone.now)

