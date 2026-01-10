import os, boto3, logging, json

SECURITY_GROUP_ID = os.environ["SECURITY_GROUP_ID"]

ec2 = boto3.client("ec2")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_security_group_info():
    response = ec2.describe_security_groups(GroupIds=[SECURITY_GROUP_ID])
    return response["SecurityGroups"][0]

def get_rule_to_invoke(security_group_info, port, protocol, cidr):
    for rule in security_group_info.get("IpPermissions", []):
        if(
            rule.get("FromPort") == port 
            and rule.get("ToPort") == port 
            and rule.get("IpProtocol") == protocol 
        ):
            for ip_range in rule.get("IpRanges", []):
                if ip_range.get("CidrIp") == cidr:
                    return {
                        "IpProtocol": protocol,
                        "FromPort": port,
                        "ToPort": port,
                        "IpRanges": [{"CidrIp": cidr}]
                    }

def revoke_inbound_rule_from_security_group(inbound_rule_to_revoke):
    ec2.revoke_security_group_ingress(
        GroupId=SECURITY_GROUP_ID,
        IpPermissions=[inbound_rule_to_revoke]
    )

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    input = event["Input"]
    user_ip = input["userIp"]
    cidr = f"{user_ip}/32"
    port = 22
    protocol = "tcp"
    logger.info(f"Revoking inbound rule for {cidr} from security group with id: {SECURITY_GROUP_ID}")
    try:
        security_group_info = get_security_group_info()
        inbound_rule_to_revoke = get_rule_to_invoke(security_group_info, port, protocol, cidr)
        if not inbound_rule_to_revoke:
            logger.info("No matching inbound rule found")
            return "Fail"
        revoke_inbound_rule_from_security_group(inbound_rule_to_revoke)
        logger.info("Inbound rule revoked")
        return "Success"
    except Exception as e:
        logger.info("Exception when revoking rule from security group")
        logger.info(e)
        return "Fail"