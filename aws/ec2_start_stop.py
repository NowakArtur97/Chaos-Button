import os, boto3, json

region = os.environ['AWS_REGION']
instance = 'i-0cedabd143bbe3e2c'
ec2 = boto3.client('ec2', region_name=region)

def start_ec2_instance():
    ec2.start_instances(InstanceIds=[instance])
    print('Successfully started EC2 instance: ' + instance)

def stop_ec2_instance():
    ec2.stop_instances(InstanceIds=[instance])
    print('Successfully stopped EC2 instance: ' + instance)

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
    