# importing customLogger
from customLogger import *

logger = CustomLog("eu-west-3", "custom-group", "custom-stream","%y-%m-%d %H:%M:%S")

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
                logger.send_log_to_cloudWatch(error_message, "error")
                return
        elif operator == "%":
            result = num1 % num2
            operation = "Modulus"
    else:
        error_message = "Invalid operator"
        logger.send_log_to_cloudWatch(error_message, "error")
        return
    info_message = f"Result of {operation}: {result} "
    logger.send_log_to_cloudWatch(info_message, "info")
    debug_message = f"{operation} operation performed"
    logger.send_log_to_cloudWatch(debug_message, "debug")


operators = {
    '+': "Addition",
    '-': "Subtraction",
    '*': "Multiplication",
    "/": "Division",
    '%': "Modulus"
}

try:
    num1 = float(input("Enter the first number: "))
    debug_message = f"User entered {num1}"
    info_message = f"{num1} pressed "
    logger.send_log_to_cloudWatch(info_message, "info")
    logger.send_log_to_cloudWatch(debug_message, "debug")

    num2 = float(input("Enter the second number: "))
    debug_message = f"User entered {num2} "
    info_message = f"{num2} pressed "
    logger.send_log_to_cloudWatch(info_message, "info")
    logger.send_log_to_cloudWatch(debug_message, "debug")

    operator = input("Enter an operator ( +, -, *, /, % ): ")

    if operator in operators:
        info_message = f"{operator} pressed "
        logger.send_log_to_cloudWatch(info_message, "info")
        calculate_result(operator)
    else:
         error_message = "Invalid operator"
         logger.send_log_to_cloudWatch(error_message, "error")

except ValueError:
     error_message = "Invalid input, enter the correct number"
     logger.send_log_to_cloudWatch(error_message, "error")

