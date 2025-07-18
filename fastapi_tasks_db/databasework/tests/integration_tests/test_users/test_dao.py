import pytest

from fastapi_tasks_db.databasework.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email, exists",
    [
        (1, "fedor@moloko.ru", True),
        (2, "anna@example.com", True),
        (4, "feo@email.com", False),
    ],
)
async def test_find_user_by_id(user_id, email, exists):
    user = await UsersDAO.find_by_id(user_id)
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
