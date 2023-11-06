import logging
import datetime
# provides an interface for interacting with AWS services
import boto3
import time


class CustomLog():
    def __init__(self, aws_region, log_group_name, log_stream_name, fmt = '%Y-%m-%d %H:%M:%S'):
        self.aws_region = aws_region

        #  A log group is a collection of log streams that have the same retention, monitoring, and access control settings. 
        self.log_group_name = log_group_name
        
        # A log stream is a sequence of log events that share the same source.
        self.log_stream_name = log_stream_name

        self.fmt = fmt
        #  client object provides methods for interacting with the CloudWatch Logs service, such as creating log groups and streams, putting log events, and querying log data.
        self.cloudwatch = boto3.client("logs", region_name = self.aws_region)
    
        try:
           self.cloudwatch.create_log_group(logGroupName = self.log_group_name)
        except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
            pass

        try:
           self.cloudwatch.create_log_stream(logGroupName = self.log_group_name, logStreamName = self.log_stream_name)
        except self.cloudwatch.exceptions.ResourceAlreadyExistsException:
           pass

        logger = logging.getLogger(__name__)

        formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
    
    # function to take log messages and log level.
    def send_log_to_cloudWatch(self, log_message, log_level):
        log_level = log_level.upper()
        # uploads a batch of log events to the specified log stream in CloudWatch Logs.
        response = self.cloudwatch.put_log_events(
            logGroupName = self.log_group_name,
            logStreamName = self.log_stream_name,
            logEvents = [
                {
                   'timestamp': int(time.time() * 1000),
                   'message': f"[{log_level}] {log_message} at {datetime.datetime.now().strftime(self.fmt)}" 
                }
            ]
        )
        return response







