from os.path import abspath, dirname

from aws_cdk import Stack
from constructs import Construct


class EksStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    def build(self):

        return self
