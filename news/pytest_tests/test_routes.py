"""Строка документации блока."""

from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'users:login',
        'users:logout',
        'users:signup'
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name):
    """Страница видна анонимному пользователю."""
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_avability(client, news):
    """Отдельная страница новости видна анонимному пользователю."""
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('auth_reader'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('auth_author'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_availability_edit_delete(parametrized_client, name,
                                  comment, expected_status):
    """Доступность страницы изменения и удаления комментария."""
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_reditect_for_client(client, name, comment):
    """Переадресация на страницу авторизации для анонимного пользователя."""
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
