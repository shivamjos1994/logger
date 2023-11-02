import logging
import datetime

from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
    set_logger_provider,
)
#  to send logging related telemetry to Azure Monitor.
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

# collects log records in a buffer and exports them periodically or when the buffer is full.
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# for creating and managing Logger instances. 
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

exporter = AzureMonitorLogExporter()

logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# LoggingHandler class forwards log records from the logging module to the OpenTelemetry logger provider.
handler = LoggingHandler()

fmt = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)


# formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

# attaching LoggingHandler to root logger.
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)


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
                logger.error("Can not divide by Zero")
                return
        elif operator == "%":
            result = num1 % num2
            operation = "Modulus"
    else:
        logger.error("Invalid operator")
        return
    logger.info(f"Result of {operation}: {result} at {datetime.datetime.now().strftime(fmt)}")
    logger.debug(f"{operation} operation performed")


operators = {
    '+': "Addition",
    '-': "Subtraction",
    '*': "Multiplication",
    "/": "Division",
    '%': "Modulus"
}

try:
    num1 = float(input("Enter the first number: "))
    logger.debug("User entered the first number")
    logger.info(f"{num1} pressed at {datetime.datetime.now().strftime(fmt)}")

    num2 = float(input("Enter the second number: "))
    logger.debug("User entered the second number ")
    logger.info(f"{num2} pressed at {datetime.datetime.now().strftime(fmt)}")

    operator = input("Enter an operator ( +, -, *, /, % ): ")

    if operator in operators:
        logger.info(f"{operator} pressed at {datetime.datetime.now().strftime(fmt)}")
        calculate_result(operator)
    else:
        logger.error("Invalid operator")

except ValueError:
    logger.error("Invalid input, enter the correct number")

