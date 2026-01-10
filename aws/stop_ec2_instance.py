import os, boto3

REGION = os.environ['AWS_REGION']
EC2_INSTANCE_ID = os.environ["EC2_INSTANCE_ID"]
ec2 = boto3.client('ec2', region_name=REGION)

def stop_ec2_instance():
    ec2.stop_instances(InstanceIds=[EC2_INSTANCE_ID])
    print('Successfully stopped EC2 instance: ' + EC2_INSTANCE_ID)

def lambda_handler(event, context):
    try:
        stop_ec2_instance()
        return "Success"
    except Exception as e:
        print("Exception when stopping EC2 instance")
        print(e)
        return "Fail"
    