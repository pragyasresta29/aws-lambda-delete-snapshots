import json
from aws import snapshot_manager, aws_service


def lambda_handler(event, context):
    print("===========DELETING UNUSED AMI============")
    snapshot_manager.delete_unused_amis()
    print("===========DELETION COMPLETE===========")
    print("===========DELETING UNUSED SNAPSHOTS============")
    snapshot_manager.delete_unused_snapshots()
    print("===========DELETION COMPLETE===========")

    return {
        'statusCode': 200,
        'body': 'Deletion complete'
    }
