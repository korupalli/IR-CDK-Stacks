import boto3
from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as _s3,
    aws_s3_notifications,
    core
)

class IrAPI01Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        s3 = _s3.Bucket(self, "testbuckforall")
        print(s3)
        
        lambda_dir_path = os.path.join(os.getcwd(), "ir_cdk_stacks", "IN-API-01")
        function = _lambda.Function(self, "lambda_function",
                                    runtime=_lambda.Runtime.PYTHON_2_7, memory_size = 512, #timeout=core.Duration(120),
                                    handler="parser.lambda_handler",
                                    code=_lambda.Code.asset(lambda_dir_path))
                                    
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["s3:*"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["waf-regional:UpdateIPSet","waf-regional:GetIPSet","waf-regional:GetChangeToken"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["logs:*"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["cloudformation:DescribeStacks"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["SNS:Publish"],
                    effect=iam.Effect.ALLOW,
                    resources=["arn:aws:sns:us-east-1:544820149332:IN-API-01-IPBlocked"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["cloudwatch:PutMetricData"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )
        function.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["lambda:*"],
                    effect=iam.Effect.ALLOW,
                    resources=["*"],
                )
            )

        # create s3 notification for lambda function
        notification = aws_s3_notifications.LambdaDestination(function)

        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)
