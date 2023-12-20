from httpx import AsyncClient
from fastapi.testclient import TestClient
from service.modules.api.users import router
client = TestClient(router)


async def test_user_create(client: AsyncClient):
    resp = await client.post('user/register/test-user')

    assert resp.status_code == 200


async def test_get_user(client: AsyncClient, user_1_session, username_1):
    resp = await client.get('user/whoami', headers={'Cookie': f'cookie={user_1_session}'})

    assert resp.status_code == 200
    data = resp.json()
    assert data['username'] == username_1


async def test_file_download(client: AsyncClient):
    resp = await client.get('/file/download', params={'filename': 'test_file.txt'})

    assert resp.status_code == 200
    assert resp.headers['Content-Disposition'] == 'attachment; filename="test_file.txt"'
    assert resp.headers['Content-Type'] == 'text/plain'


async def test_file_upload(client: AsyncClient):
    files = {'file': ('test_file.txt', open('test_file.txt', 'rb'), 'text/plain')}
    resp = await client.post('/file/upload', files=files)

    assert resp.status_code == 200
    assert resp.json() == {'message': 'File uploaded successfully'}


async def test_folder_access(client: AsyncClient):
    resp = await client.get('/folder/access', params={'folder_id': '12345'})

    assert resp.status_code == 200
    assert resp.json() == {'message': 'User has access to the folder'}


async def test_list_folders(client: AsyncClient):
    resp = await client.get('/folder/list')

    assert resp.status_code == 200
    assert resp.json() == {'folders': ['folder1', 'folder2', 'folder3']}
