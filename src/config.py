from os import environ


class Config:

    # Application settings
    application_name: str = environ.get("APPLICATION_NAME", 'Application Name')

    # AWS connection
    aws_access_key: str = environ.get("AWS_ACCESS_KEY")
    aws_access_key_secret: str = environ.get("AWS_ACCESS_KEY_SECRET")
    aws_region_name: str = environ.get("AWS_REGION_NAME")

    # AWS Dynamo DB
    dynamo_table_name: str = environ.get("DYNAMO_TABLE_NAME", "2fa_authenticators")
    dynamo_partition_key: str = environ.get("DYNAMO_PARTITION_KEY", "secret_id")


config = Config()
