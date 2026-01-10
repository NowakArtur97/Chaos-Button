import os, boto3, logging, json

SECURITY_GROUP_ID = os.environ["SECURITY_GROUP_ID"]

ec2 = boto3.client("ec2")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def restore_inbound_rule_in_security_group(previous_rule):
    ec2.authorize_security_group_ingress(
        GroupId=SECURITY_GROUP_ID,
        IpPermissions=[previous_rule]
    )

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    previous_rule = event["previousRule"]
    try:
        restore_inbound_rule_in_security_group(previous_rule)
        return "Success"
    except Exception as e:
        logger.info("Exception when restoring rule in security group")
        logger.info(e)
        return "Fail"
