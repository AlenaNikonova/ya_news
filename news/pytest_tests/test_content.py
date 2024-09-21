"""Строка документации блока."""

from django.urls import reverse

import pytest

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count_on_homepage(client, list_news):
    """Тест пагинации."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    """Сортировка новостей."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(list_comment, news, client, url_detail):
    """Сортировка комментариев."""
    response = client.get(url_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news, url_detail):
    """Анонимный пользователь не видит формы создания комментария."""
    response = client.get(url_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(news, auth_reader, url_detail):
    """Авторизованному пользователю видна форма создания комментария."""
    response = auth_reader.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
