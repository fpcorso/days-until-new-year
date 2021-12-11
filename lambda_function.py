import boto3


def lambda_handler(event, context):
    """Main Lambda function"""
    return


def get_twitter_keys():
    """Retrieve secrets from Parameter Store."""
    # Create our SSM Client.
    aws_client = boto3.client('ssm')

    # Get our parameter
    response = aws_client.get_parameter(
        Name='example_secret',
        WithDecryption=True
    )

    return response['Parameter']['Value']
