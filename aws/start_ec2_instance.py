import os, boto3, logging, json

REGION = os.environ['AWS_REGION']
EC2_INSTANCE_ID = os.environ["EC2_INSTANCE_ID"]

ec2 = boto3.client('ec2', region_name=REGION)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def start_ec2_instance():
    ec2.start_instances(InstanceIds=[EC2_INSTANCE_ID])
    logger.info(f'Successfully started EC2 instance: {EC2_INSTANCE_ID}')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        start_ec2_instance()
        return "Success"
    except Exception as e:
        logger.info("Exception when starting EC2 instance")
        logger.info(e)
        return "Fail"
