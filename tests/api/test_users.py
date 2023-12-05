from httpx import AsyncClient


async def test_user_create(client: AsyncClient):
    resp = await client.post('user/register/test-user')

    assert resp.status_code == 200


async def test_get_user(client: AsyncClient, user_1_session, username_1):
    resp = await client.get('user/whoami', headers={'Cookie': f'cookie={user_1_session}'})

    assert resp.status_code == 200
    data = resp.json()
    assert data['username'] == username_1
