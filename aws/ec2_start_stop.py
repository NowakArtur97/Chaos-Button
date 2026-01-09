import os, boto3, json

region = os.environ['AWS_REGION']
instance = 'i-0cedabd143bbe3e2c'
ec2 = boto3.client('ec2', region_name=region)

def stop_ec2_instance():
    ec2.stop_instances(InstanceIds=[instance])
    print('Successfully stopped instance: ' + instance)

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    input = event["Input"]
    action = input["action"]
    try:
        if action == "STOP":
            stop_ec2_instance()
            return "Success"
    except Exception as e:
        print("Exception when starting ec2 instance")
        print(e)
        return "Fail"
    print("Unknown action: " + action)
    return "Fail"
    