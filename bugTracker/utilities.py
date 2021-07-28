from enum import Enum, IntEnum
from typing import Dict, Union, Any, List

import pydantic
from django.conf import settings
from django.core import mail
from django.core.mail import send_mass_mail


class ResponseMessages(str, Enum):
    FAILED_CREATED_TASK = "Could not create task {0}"
    DELETED_TASK = 'Deleted task {0} successully'
    CREATED_TASK = 'Created task {0} successfully'
    MISSING_TASK_FIELDS = 'The following fields are missing: {0}'
    ERROR_OCCURED = 'An error occured {0}'
    TASK_NOT_EXIST = 'The task with id {0} does not exist on our system'


class ResponseCode(IntEnum):
    """Response Codes"""
    SUCCESS = 200
    FAILED = 201
    INTERNAL_SERVER_ERROR = 500
    NOT_FOUND = 404


class BaseResponse(pydantic.BaseModel):
    """Generic response format containing response code and response message"""
    response_code: int
    response_message: str
    data: Any = {}

    @classmethod
    def get_error_response(cls, e: Union[BaseException, str]):
        """Default error response"""
        return cls(response_code=ResponseCode.INTERNAL_SERVER_ERROR, response_message=str(e)).dict()

    @classmethod
    def get_success_response(cls, message: str = None, data=None):
        """Default success response"""
        data = data if data is not None else {}
        message = message if message is not None else "Successful"
        response = cls(response_code=ResponseCode.SUCCESS, response_message=message).dict()
        response["data"] = data
        return response

    @classmethod
    def get_not_found_response(cls, message: str):
        """Default not found response"""
        return cls(response_code=ResponseCode.NOT_FOUND, response_message=message).dict()

    @classmethod
    def get_failed_response(cls, message: str):
        """Default not found response"""
        return cls(response_code=ResponseCode.FAILED, response_message=message).dict()


def send_notification_email(emails: List[str], subject, message):
    datatuples = []
    for email in emails:
        datatuples.append((subject, message, settings.DEFAULT_FROM_EMAIL, [email]))
    send_count = send_mass_mail(datatuples, fail_silently=True)
    if send_count != len(emails):
        print("Not all emails were sent")
