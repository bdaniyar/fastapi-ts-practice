import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password,status_code",
    [
        ("new_user@example.com", "kotopes", 200),
        ("new_user@example.com", "kot0pes", 409),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password,status_code", [("new_user@example.com", "kotopes", 200)]
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
