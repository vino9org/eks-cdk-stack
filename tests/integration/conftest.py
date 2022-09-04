import os
from typing import List

import boto3
import pytest  # noqa: F401
from botocore.exceptions import ClientError


_stack_outputs_: List[str] = {}





def stack_outputs_for_key(key: str) -> List[str]:
    """
    helper funciton to get output values from a Cloudformation stack
    can be used by a fixture to retrieve output values and inject
    into tests

    e.g.

    # in conftest.py
    @pytest.fixture(scope="session")
    def api_base_url() -> str:
        return stack_outputs_for_key("RestApiEndpoint")[0]

    # in tests
    import requests
    def test_restapi(api_base_url):
        response = requests.get(f"{api_base_url}/ping")
        assert response.status_code == 200

    """

    global _stack_outputs_

    region = os.environ.get("TESTING_REGION", "us-west-2")
    stack_name = os.environ.get("TESTING_STACK_NAME", "EksStack")
    client = boto3.client("cloudformation", region_name=region)

    if not _stack_outputs_:
        try:
            response = client.describe_stacks(StackName=stack_name)
            _stack_outputs_ = response["Stacks"][0]["Outputs"]  # type: ignore
        except ClientError as e:
            raise Exception(f"Cannot find stack {stack_name} in region {region}") from e

    output_values = [item["OutputValue"] for item in _stack_outputs_ if key in item["OutputKey"]]
    if not output_values:
        raise Exception(f"There is no output with key {key} in stack {stack_name} in region {region}")

    return output_values