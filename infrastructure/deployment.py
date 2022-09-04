import os

import aws_cdk as cdk

from eks_stack import EksStack

stack_name = os.environ.get("TESTING_STACK_NAME", "EksStack")
app = cdk.App()
EksStack(app, stack_name).build()
app.synth()
