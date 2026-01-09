import os, boto3, json

REGION = os.environ['AWS_REGION']
EC2_INSTANCE_ID = os.environ["EC2_INSTANCE_ID"]
ec2 = boto3.client('ec2', region_name=REGION)

def start_ec2_instance():
    ec2.start_instances(InstanceIds=[EC2_INSTANCE_ID])
    print('Successfully started EC2 instance: ' + EC2_INSTANCE_ID)

def stop_ec2_instance():
    ec2.stop_instances(InstanceIds=[EC2_INSTANCE_ID])
    print('Successfully stopped EC2 instance: ' + EC2_INSTANCE_ID)

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    input = event["Input"]
    action = input["action"]
    try:
        if action == "START":
            start_ec2_instance()
            return "Success"
    except Exception as e:
        print("Exception when starting EC2 instance")
        print(e)
        return "Fail"
    try:
        if action == "STOP":
            stop_ec2_instance()
            return "Success"
    except Exception as e:
        print("Exception when stopping EC2 instance")
        print(e)
        return "Fail"
    print("Unknown action: " + action)
    return "Fail"
    