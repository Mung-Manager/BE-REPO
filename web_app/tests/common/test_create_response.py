from mung_manager.common.response import create_response
from rest_framework import status


def test_create_response():
    custom_data = {"key": "custom_value"}
    response = create_response(
        data=custom_data,
        status_code=status.HTTP_200_OK,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["code"] == "request_success"
    assert response.data["success"] is True
    assert response.data["message"] == "Request was successful."
    assert response.data["data"] == custom_data
