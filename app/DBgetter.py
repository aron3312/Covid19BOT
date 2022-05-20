import boto3
import botocore

class DynamodbTable(object):
    """
    For connecting dynamodb and get data from table
    """
    def __init__(self, table_name):
        client = boto3.resource('dynamodb')
        self.tb = client.Table(table_name)

    def get_all_data(self):
        scan_kwargs = {}
        complete = False
        records = []
        while not complete:
            try:
                response = self.tb.scan(**scan_kwargs)
            except botocore.exceptions.ClientError as error:
                raise Exception('Error quering DB: {}'.format(error))

            records.extend(response.get('Items', []))
            next_key = response.get('LastEvaluatedKey')
            scan_kwargs['ExclusiveStartKey'] = next_key
            complete = True if next_key is None else False
        return records

    def get_unique_key(self, col_name):
        resp = self.tb.scan(AttributesToGet=[col_name])
        result = [r[col_name] for r in resp["Items"]]
        return result