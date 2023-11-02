import logging
import datetime
# provides an interface for interacting with AWS services
import boto3
import time

# configure the aws region (Mumbai)
aws_region = "ap-south-1"


fmt = '%Y-%m-%d %H:%M:%S'

# creating a cloudwatch to log client
#  client object provides methods for interacting with the CloudWatch Logs service, such as creating log groups and streams, putting log events, and querying log data.
cloudwatch = boto3.client("logs", region_name = aws_region)

# creating cloudwatch log group an stream if they don't already exist.

#  A log group is a collection of log streams that have the same retention, monitoring, and access control settings. 
log_group_name = "Calculation-app"

# A log stream is a sequence of log events that share the same source.
log_stream_name = "Calculation-stream"

try:
    cloudwatch.create_log_group(logGroupName = log_group_name)
except cloudwatch.exceptions.ResourceAlreadyExistsException:
    pass

try:
    cloudwatch.create_log_stream(logGroupName = log_group_name, logStreamName = log_stream_name)
except cloudwatch.exceptions.ResourceAlreadyExistsException:
    pass

logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


# function to take log messages and log level.
def send_log_to_cloudWatch(log_message, log_level):
    log_level = log_level.upper()
    # uploads a batch of log events to the specified log stream in CloudWatch Logs.
    response = cloudwatch.put_log_events(
        logGroupName = log_group_name,
        logStreamName = log_stream_name,
        logEvents = [
            {
               'timestamp': int(time.time() * 1000),
               'message': f"[{log_level}] {log_message}"
            }
        ]
    )
    return response


def calculate_result(operator):
    if num1 is not None and num2 is not None:
        if operator == "+":
            result = num1 + num2
            operation = "Addition"
        elif operator == "-":
            result = num1 - num2
            operation = "Subtraction"
        elif operator == "*":
            result = num1 * num2
            operation = "Multiplication"
        elif operator == "/":
            try:
                result = num1 / num2
                operation = "Division"
            except ZeroDivisionError:
                error_message = "Can not divide by Zero"
                send_log_to_cloudWatch(error_message, "error")
                return
        elif operator == "%":
            result = num1 % num2
            operation = "Modulus"
    else:
        error_message = "Invalid operator"
        send_log_to_cloudWatch(error_message, "error")
        return
    info_message = f"Result of {operation}: {result} at {datetime.datetime.now().strftime(fmt)}"
    send_log_to_cloudWatch(info_message, "info")
    debug_message = f"{operation} operation performed"
    send_log_to_cloudWatch(debug_message, "debug")


operators = {
    '+': "Addition",
    '-': "Subtraction",
    '*': "Multiplication",
    "/": "Division",
    '%': "Modulus"
}

try:
    num1 = float(input("Enter the first number: "))
    debug_message = "User entered the first number"
    info_message = f"{num1} pressed at {datetime.datetime.now().strftime(fmt)}"
    send_log_to_cloudWatch(info_message, "info")
    send_log_to_cloudWatch(debug_message, "debug")

    num2 = float(input("Enter the second number: "))
    debug_message = "User entered the second number "
    info_message = f"{num2} pressed at {datetime.datetime.now().strftime(fmt)}"
    send_log_to_cloudWatch(info_message, "info")
    send_log_to_cloudWatch(debug_message, "debug")

    operator = input("Enter an operator ( +, -, *, /, % ): ")

    if operator in operators:
        info_message = f"{operator} pressed at {datetime.datetime.now().strftime(fmt)}"
        send_log_to_cloudWatch(info_message, "info")
        calculate_result(operator)
    else:
         error_message = "Invalid operator"
         send_log_to_cloudWatch(error_message, "error")

except ValueError:
     error_message = "Invalid input, enter the correct number"
     send_log_to_cloudWatch(error_message, "error")

