"""Строка документации блока."""

from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.test.client import Client

import pytest

from yanews import settings
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    """Автор."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def auth_author(author):
    """Аутентифицированный автор."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    """Пользователь."""
    return django_user_model.objects.create(username='Просто читатель')


@pytest.fixture
def auth_reader(reader):
    """Аутентифицированный пользователь."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    """Новость."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def list_news():
    """Список новостей."""
    now = timezone.now()
    all_news = [
            News(title=f'Новость {index}', text='Просто текст.',
                 date=now - timedelta(days=index))
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(news, author):
    """Комментарий."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def list_comment(news, author):
    """Список комментариев."""
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news


@pytest.fixture
def url_detail(news):
    """URL для страницы отдельной новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_delete(comment):
    """URL для страницы удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_edit(comment):
    """URL для страницы изменения комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def form_data():
    """Форма."""
    return {'text': 'Новый текст'}
