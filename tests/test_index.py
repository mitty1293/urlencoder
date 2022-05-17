import pytest
from urlencoder.application import app


def test_index_get():
    app.config["TESTING"] = True
    rv = app.test_client().get("/")
    assert rv.status_code == 200


text_list = [
    ("test", "test"),
    ("テスト", "%E3%83%86%E3%82%B9%E3%83%88"),
    ("http://example.com", "http://example.com"),
]


@pytest.mark.parametrize(("input", "output"), text_list)
def test_index_post_encode(input, output):
    app.config["TESTING"] = True
    rv = app.test_client().post(
        "/", data=dict(inputtext=input, encode_btn="", outputtext="")
    )
    assert output in rv.data.decode()


@pytest.mark.parametrize(("output", "input"), text_list)
def test_index_post_decode(output, input):
    app.config["TESTING"] = True
    rv = app.test_client().post(
        "/", data=dict(inputtext=input, decode_btn="", outputtext="")
    )
    assert output in rv.data.decode()
