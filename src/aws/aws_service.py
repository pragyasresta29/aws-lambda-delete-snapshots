import boto3


def get_ec2_client():
    return boto3.client('ec2')


def get_ec2_resource():
    return boto3.resource('ec2')


def describe_snapshots():
    snapshot_collection = get_ec2_client().describe_snapshots(OwnerIds=['self'])
    return snapshot_collection['Snapshots']


def describe_images():
    ami_collection = get_ec2_client().describe_images(Owners=['self'])
    return ami_collection['Images']


def delete_snapshot(snapshot_id):
    snapshot = get_ec2_resource().Snapshot(snapshot_id)
    return snapshot.delete(
        DryRun=False
    )


def delete_unused_ami(ami_id):
    instances = fetch_instances_by_ami(ami_id)
    if (len(instances) == 0):
        print("No instances associated with ami: [%s], Deregistering..." % ami_id)
        image = get_ec2_resource().Image(ami_id)
        response = image.deregister(
            DryRun=False
        )
        return True
    return False


def fetch_instances_by_ami(ami_id):
    instance_collection = get_ec2_resource().instances.filter(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [
                    ami_id,
                ]
            },
        ],
        DryRun=False
    )
    return [instance for instance in instance_collection]

