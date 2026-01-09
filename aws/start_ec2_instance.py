import os, boto3, json

REGION = os.environ['AWS_REGION']
EC2_INSTANCE_ID = os.environ["EC2_INSTANCE_ID"]
ec2 = boto3.client('ec2', region_name=REGION)

def start_ec2_instance():
    ec2.start_instances(InstanceIds=[EC2_INSTANCE_ID])
    print('Successfully started EC2 instance: ' + EC2_INSTANCE_ID)

def lambda_handler(event, context):
    try:
        start_ec2_instance()
        return "Success"
    except Exception as e:
        print("Exception when starting EC2 instance")
        print(e)
        return "Fail"
