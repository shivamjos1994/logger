import logging
import datetime

fmt = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


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

