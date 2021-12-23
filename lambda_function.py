import boto3
import datetime
import tweepy


def lambda_handler(event, context):
    """Main Lambda function"""

    keys = get_twitter_keys()

    client = tweepy.Client(
        consumer_key=keys.get('twitter_api_key'),
        consumer_secret=keys.get('twitter_api_secret'),
        access_token=keys.get('twitter_access_token'),
        access_token_secret=keys.get('twitter_access_secret')
    )

    tweet = get_tweet()
    client.create_tweet(text=tweet)


def get_tweet() -> str:
    """Creates our tweet."""

    # Calculate days until new year's day.
    next_year = datetime.datetime.now().year + 1
    new_year = datetime.datetime(next_year, 1, 1, 0, 0, 0)
    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    days_left = (new_year - today).days

    # Customize text based on the number of days until the new year.
    if days_left == 1:
        tweet = "Tomorrow is New Year's Day!"
    elif today.month == 1 and today.day == 1:
        tweet = f'Happy New Year!! Welcome to {today.year}! Only {days_left} until next year.'
    else:
        tweet = f'There are {days_left} days until {next_year}'

    return tweet


def get_twitter_keys() -> dict:
    """Retrieve secrets from Parameter Store."""
    # Create our SSM Client.
    aws_client = boto3.client('ssm')

    # Get our keys from Parameter Store.
    parameters = aws_client.get_parameters(
        Names=[
            'twitter_api_key',
            'twitter_api_secret',
            'twitter_access_token',
            'twitter_access_secret'
        ],
        WithDecryption=True
    )

    # Convert list of parameters into simpler dict.
    keys = {}
    for parameter in parameters['Parameters']:
        keys[parameter['Name']] = parameter['Value']

    return keys
