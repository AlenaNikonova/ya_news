"""Строка документации блока."""

from http import HTTPStatus
import pytest
from pytest_django.asserts import assertFormError, assertRedirects
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Новый текст'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, url_detail, form_data):
    """Анонимный пользователь не может создать комментарий."""
    client.post(url_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_auth_user_can_create_comment(auth_reader, url_detail, form_data):
    """Аутентифицированный пользователь может создать комментарий."""
    auth_reader.post(url_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_user_cant_use_bad_words(auth_reader, url_detail):
    """Невозможно создать комментарий с запрещенными словами."""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_reader.post(url_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_not_author_cant_delete_comment(auth_reader, url_delete):
    """НЕ автор не может удалить чужой комментарий."""
    response = auth_reader.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_author_can_delete_comment(auth_author, url_delete, url_detail):
    """Автор может удалить свой комментарий."""
    response = auth_author.delete(url_delete)
    url_to_comments = url_detail + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_not_author_cant_edit_comment(auth_reader, url_edit, comment):
    """НЕ автор не может изменить чужой комментарий."""
    response = auth_reader.post(url_edit)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT


@pytest.mark.django_db
def test_author_can_edit_comment(auth_author, url_edit,
                                 url_detail, comment, form_data):
    """Автор может изменить свой комментарий."""
    response = auth_author.post(url_edit, data=form_data)
    url_to_comments = url_detail + '#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT
