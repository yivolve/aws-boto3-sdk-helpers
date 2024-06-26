import sys
from datetime import datetime
import botocore
sys.path.append( '../')
from common.args import cloudwatch_logs_args  ## This is the only variable we should be importing from the args module and pass it to the functions below
from common.boto_client_declaration import cloudwatch_logs_client
from common.exceptions import common
from common.banners import operation_start_msg, outcome_banner
from common.logging_setup import logger

args, logs = cloudwatch_logs_args(), cloudwatch_logs_client(cloudwatch_logs_args())

def cloudwatch_delete_log_group(args):
    f"""
    Calls the necessary functions to delete a given CloudWatch log group.\n

    Example
    -------
    cloudwatch_delete_log_groups(cloudwatch_logs_args_call)

    Parameters
    ------------
        args: argparse.Namespace\n
        The argparse generated by the ../common/args.py script, the best this is to import the 'cloudwatch_logs_args_call' variable from it.
    """
    start_time = datetime.now()
    action, resource = "'Delete CloudWatch'", "group"
    operation_start_msg(action, args.group_name, resource)
    return_code = search_log_groups(args.group_name) ## Objects are remove with this call
    if (return_code == 0 and args.dry_run):
        logger.info(f"The {args.group_name} log group was found but will not be deleted, to delete it set the --dry-run flag to False")
    elif (return_code == 0 and not args.dry_run):
        logger.info(f"Proceeding to delete the {args.group_name} log group")
        return_code =  cloudwatch_delete_log_group_execution(args.group_name)

    total_time =  datetime.now() - start_time
    outcome_banner(action, args.group_name, resource, return_code, total_time)

def search_log_groups(group_name=""):
    try:
        response = logs.describe_log_groups(
            limit=50,
            logGroupNamePrefix=group_name
        )
        # logger.info(response)
        if not response["logGroups"]:
            logger.error("The log group doesn't exist")
            return 1
        return 0
    except botocore.exceptions.ClientError as error_found:
        if error_found.response['Error']['Code'] in common:
            logger.error(f"Error Code: {format(error_found.response['Error']['Code'])}")
            logger.error(f"Error Code: {format(error_found.response['Error']['Code'])}")
            logger.error(f"Message: {format(error_found.response['Error']['Message'])}")
            logger.error(f"Request ID: {format(error_found.response['ResponseMetadata']['RequestId'])}")
            logger.error(f"Http code: {format(error_found.response['ResponseMetadata']['HTTPStatusCode'])}")
        else:
            logger.error(f"Error occured : {error_found}")
        return 1


def cloudwatch_delete_log_group_execution(group_name=""):
    """
    Description
    -----------
    Deletes CloudWatch log groups.

    See more about this operation at:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_group.html
    """
    if not group_name:
        logger.error("No log group name was provided, exiting")
        return 1
    try:
        logs.delete_log_group(logGroupName=group_name)
        return 0
    except botocore.exceptions.ClientError as error_found:
        if error_found.response['Error']['Code'] in common:
            logger.error(f"Error Code: {format(error_found.response['Error']['Code'])}")
            logger.error(f"Error Code: {format(error_found.response['Error']['Code'])}")
            logger.error(f"Message: {format(error_found.response['Error']['Message'])}")
            logger.error(f"Request ID: {format(error_found.response['ResponseMetadata']['RequestId'])}")
            logger.error(f"Http code: {format(error_found.response['ResponseMetadata']['HTTPStatusCode'])}")
        else:
            logger.error(f"Error occured : {error_found}")
        return 1

if __name__ == "__main__":
    cloudwatch_delete_log_group(args)
    # delete_bucket_objects_excecution()
