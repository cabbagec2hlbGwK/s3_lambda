import boto3
import json
import uuid
import time


def main(a, b):
    print(f"this is a test script {a['Records'][0]['s3']['bucket']['arn']}")
    s3 = boto3.client('s3')
    file = s3.get_object(Bucket=a['Records'][0]['s3']['bucket']
                         ['name'], Key=a['Records'][0]['s3']['object']['key'])
    process(s3=s3, file=" ",
            bucket=a['Records'][0]['s3']['bucket'])


def process(s3, file, bucket):
    print("creating manifest")
    manifest_data = {
        "fileLocations": [
            {
                "URIs": [
                    f"s3://{bucket}/test.csv"
                ]
            }
        ],
        "globalUploadSettings": {
            "format": "CSV",
            "delimiter": ",",
            "textqualifier": "\"",
            "containsHeader": "true"
        }
    }
    try:
        s3.put_object(
            Bucket=bucket,
            Key="manifest.json",
            Body=str(json.dumps(manifest_data))
        )
        print("done")
        create_data_source(bucket_name=bucket, key=None)
    except Exception as e:
        print(f"Error: {e}")


def create_data_source(bucket_name, key):
    account_no = "536380612665"
    dataSourceID = str(uuid.uuid4())
    quicksight = boto3.client('quicksight')

    response = quicksight.create_data_source(
        AwsAccountId=account_no,
        DataSourceId=dataSourceID,
        Name='testDataSource',
        Type='S3',
        DataSourceParameters={
            'S3Parameters': {
                'ManifestFileLocation': {
                    'Bucket': bucket_name,
                    'Key': 'manifest.json'
                }
            }
        },
    )
    print(response)
    time.sleep(5)
    create_data_set(account_id=account_no, dataSource_id=dataSourceID)


def create_data_set(account_id, dataSource_id):
    dataSet_id = "kksasd"+str(uuid.uuid4())
    quicksight_client = boto3.client('quicksight')

    # Create the dataset
    dataset_config = {
        'AwsAccountId': account_id,
        'DataSetId': dataSet_id,
        'Name': 'kk1',
        'PhysicalTableMap': {
            'YourTableAlias': {
                'S3Source': {
                    'DataSourceArn': f'arn:aws:quicksight:us-east-1:{account_id}:datasource/{dataSource_id}',
                    'UploadSettings': {
                        'Format': 'CSV',
                        'StartFromRow': 1,
                        'ContainsHeader': True
                    },
                    'InputColumns': [
                        {
                            'Name': 'Product_id',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'Title',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'availability',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'brand',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'categories',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'price',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'seller_id',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'seller_name',
                            'Type': 'STRING'
                        },
                        {
                            'Name': 'url',
                            'Type': 'STRING'
                        },
                    ]
                }
            }
        },
        'ImportMode': 'SPICE',
    }
    response = quicksight_client.create_data_set(**dataset_config)

    # Print the response
    print(response)

    response = quicksight_client.create_ingestion(
        AwsAccountId=account_id,
        DataSetId=dataSet_id,
        IngestionId=f'injest-{str(uuid.uuid4())}'
    )

    print(response)


def change_permision():
    quicksight = boto3.client('quicksight')

    dataset_arn = 'arn:aws:quicksight:us-east-1:536380612665:dataset/kksasdf7fb4a55-27a0-4d46-830f-f2556a43593c'

    # Define the permissions to grant to all authenticated users
    permissions = [
        {
            "Effect": "Allow",
            'Actions': [
                'quicksight:DescribeDataSet',
                'quicksight:DescribeDataSetPermissions',
                'quicksight:PassDataSet',
            ],
            "Resource": dataset_arn
        }
    ]

    # Update permissions for the dataset
    response = quicksight.update_data_set_permissions(
        AwsAccountId='536380612665',
        DataSetId='kksasdf7fb4a55-27a0-4d46-830f-f2556a43593c',
        GrantPermissions=permissions
    )

    print(response)
