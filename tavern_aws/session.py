import logging

import boto3
import requests
from requests_aws4auth import AWS4Auth
from tavern._core import exceptions
from tavern._core.dict_util import check_expected_keys

logger = logging.getLogger(__name__)


class AWSSession(requests.Session):
    def __init__(self, **kwargs):
        super().__init__()

        expected_blocks = {
            "profile",
            "service",
            "region",
        }
        check_expected_keys(expected_blocks, kwargs)

        try:
            profile = kwargs["profile"]
            session = boto3.Session(profile_name=profile)
            credentials = session.get_credentials()
            if credentials is None:
                raise RuntimeError("No credentials found")
            auth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                kwargs["region"],
                kwargs["service"],
                aws_session_token=credentials.token,
            )
            self.auth = auth
        except KeyError as e:
            msg = "Need to specify aws profile"
            logger.error(msg)
            raise exceptions.MissingKeysError(msg) from e

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass
