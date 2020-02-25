from aws import aws_service
from datetime import datetime, timedelta


def get_snapshots():
    # Fetch snapshots older than 7 days
    snapshots = aws_service.describe_snapshots()
    return [snapshot for snapshot in snapshots if is_older_than_seven_days(snapshot)]


def delete_unused_amis():
    # Delete AMIs that are not attached to any ec2 instances
    amis = aws_service.describe_images()
    print("Total AMIs: %s" % len(amis))
    for ami in amis:
        aws_service.delete_unused_ami(ami['ImageId'])


def delete_unused_snapshots():
    # Deletes unused snapshots older that 7 days. 
    snapshots = get_snapshots()
    print("============================")
    print("Total Snapshots: %s" % len(snapshots))
    for snapshot in snapshots:
        try:
            aws_service.delete_snapshot(snapshot['SnapshotId'])
        except Exception:
            # Exception occurs if the snapshot is linked to an AMI. In this case, we wont delete it.
            pass


def is_older_than_seven_days(snapshot):
    start_time = snapshot['StartTime']
    timezone = start_time.tzinfo
    seven_days_earlier = datetime.now(timezone) - timedelta(days=7)
    return start_time < seven_days_earlier
