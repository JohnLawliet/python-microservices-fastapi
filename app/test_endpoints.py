from app.main import app, BASE_DIR
import pathlib
import shutil
import time
from fastapi.testclient import TestClient
from PIL import Image, ImageChops

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']
    assert response.text

def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"hello":"world"}


# glob is used to list files within a file directory path based on special character given
# def test_echo_home():
#     img_saved_path = BASE_DIR / "images"
#     for path in img_saved_path.glob("*"):
#         print("############### -> ",path)
#         response = client.post("/img-echo/", files={"file": open(path, 'rb')})
#         assert True
