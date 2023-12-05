import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse


class BaseAPIRouter(APIRouter):
    logger = logging.getLogger()


class OctetStream(StreamingResponse):
    media_type = 'application/octet-stream'
