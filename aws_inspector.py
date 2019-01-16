#!/usr/bin/python3
"""
Usage:
  aws_inspector.py -h | --help
  aws_inspector.py (--internetGateways | --instances)
 
Options:
  --test=<test> nothing here to see
"""
import json
import datetime
from dateutil.tz import tzutc
# import aws sdk
import boto3
import uuid


from docopt import docopt


def create_aws_client(aws_target: str = "ec2") -> object:
    """
    Instantiate an aws client
    """
    return boto3.client(aws_target)

def create_aws_resource(aws_target: str = "ec2") -> object:
    """
    Instantiate an aws resource
    """
    return boto3.resource(aws_target)

def create_aws_session(aws_target: str = "ec2") -> object:
    """
    Instantiate an aws session.
    """
    return boto3.session(aws_target)

def get_aws_buckets(s3client: object) -> dict:
    """
    List the aws buckets available
    """
    return s3client.list_buckets()

def list_vpcs_on_internet_gateways(ec2client: object) -> list:
    """
    List all VPCs connected to an internet gateway

    Params:
        ec2client: The boto3 ec2 client object
    
    Returns:
        A list of VPCs that are attached to internet gateways
    """
    igateways = ec2client.describe_internet_gateways()['InternetGateways']
    vpc_list = []
    for gateway in igateways:
        vpc_list.append(gateway['Attachments'][0]['VpcId'])
    return vpc_list

def list_all_instances(ec2client: object) -> list:
    """
    List all instances

    Params:
        ec2client: The boto3 ec2 client object
    
    Returns:
        A list of ec2 instances
    """
    return ec2client.describe_instances()

def list_all_image_ids_in_use(ec2client: object) -> list:
    """
    List all image IDs in use

    Params:
        ec2client: The boto3 ec2 client object
    
    Returns:
        A set of AMI IDs in use
    """
    instances = ec2client.describe_instances()
    ami_list = []
    for instance in instances['Reservations']:
        ami_list.append(instance['Instances'][0]['ImageId'])
    return set(ami_list)

def main():
    # opts = docopt(__doc__)
    ec2resource = create_aws_resource()
    # for instance in ec2resource.instances.all():
    #     print(json.dumps({"id": instance.id, "state": instance.state}, indent=4, sort_keys=True))
    ec2client = create_aws_client(aws_target="ec2")
    # print(ec2client.describe_vpcs())
    print(ec2client.describe_accounts())

if __name__ == '__main__':
    main()
