import boto3
import json
import uuid
import time
import csv

QUICKS_ACCOUNT_NO=""#!put the account id of your QUICKSIGHT

def create_csv(file,s3,bucket,name):
    csv_data = []
    content = file['Body'].read().decode('utf-8')
    data = json.loads(content)
    if isinstance(data, list):
        if data:
            keys = data[0].keys()
            data.append(keys)
            for item in data:
                csv_data.append(list(item.values()))
    else:
        pass
        # If it's not a list, handle it according to your specific JSON structure

    with open(f'/tmp/{name.replace(".json","")}.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)
    s3.upload_file(f'/tmp/{name.replace(".json","")}.csv', bucket, name.replace(".json",".csv"))

def main(a, b):
    print(f"this is a test script {a['Records'][0]['s3']['bucket']['arn']}")
    s3 = boto3.client('s3')
    file = s3.get_object(Bucket=a['Records'][0]['s3']['bucket']
                         ['name'], Key=a['Records'][0]['s3']['object']['key'])
    process(s3=s3, file=file,
            bucket=a['Records'][0]['s3']['bucket']i,name=a['Records'][0]['s3']['object']['key'])


def process(s3, file, bucket,name):
    create_csv(file=file,s3=s3,bucket=bucket,name=name)
    s3.get_object(file)
    print("creating manifest")
    manifest_data = {
        "fileLocations": [
            {
                "URIs": [
                    f"s3://{bucket}/{name.replace('.json','')}.csv"
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
    account_no = QUICKS_ACCOUNT_NO
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
        'Name': f'test:{str(uuid.uuid4())}',
        'PhysicalTableMap': {
            'YourTableAlias': {
                'S3Source': {
                    'DataSourceArn': f'arn:aws:quicksight:us-east-1:{account_id}:datasource/{dataSource_id}',
                    'UploadSettings': {
                        'Format': 'CSV',
                        'StartFromRow': 1,
                        'ContainsHeader': True
                    }
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
        AwsAccountId=QUICKS_ACCOUNT_NO,
        DataSetId='kksasdf7fb4a55-27a0-4d46-830f-f2556a43593c',
        GrantPermissions=permissions
    )

    print(response)
