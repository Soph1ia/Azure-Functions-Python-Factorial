import time
import statistics
import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    number = req.params.get('number')
    if not number:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            number = req_body.get('number')

    if number:
        output1,output2 = benchmark(number)
        return func.HttpResponse(f"The number is, {number}. throughput: {output1} average: {output2}")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a number in the query string or in the request body for a personalized response.",
            status_code=200
        )


def factorial_function(num):
    num = int(num)
    factorial = 1
    # check if the number is negative, positive or zero
    if num < 0:
        return "Sorry, factorial does not exist for negative numbers"
    else:
        for i in range(1, num + 1):
            factorial = factorial * i
        return factorial


def benchmark(num):
    throughput_time = {"factorial": []}
    average_duration_time = {"factorial": []}

    for i in range(40):  # adjust accordingly so whole thing takes a few sec
        logging.info('factorial execution beginning')
        t0 = time.time()
        factorial_function(num)
        t1 = time.time()
        logging.info('factorial function ended, calculating metrics')
        if i >= 20:  # We let it warmup for first 20 rounds, then consider the last 20 metrics
            throughput_time["factorial"].append(1 / ((t1 - t0) * 1000))
            average_duration_time["factorial"].append(((t1 - t0) * 1000) / 1)

    for name, numbers in throughput_time.items():
        logging.info("The throughput time")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        throughput_output = "FUNCTION {} used {} times. > MEDIAN {} ops/ms > MEAN {} ops/ms  > STDEV {} ops/ms".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logging.info(throughput_output)

    for name, numbers in average_duration_time.items():
        logging.info("The average Duration details")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        average_output = "FUNCTION {} used {} times. > MEDIAN {} ms/ops > MEAN {} ms/ops  > STDEV {} ms/ops".format(name,
                                                                                                            length,
                                                                                                            median,
                                                                                                            mean,
                                                                                                            stdev)
        logging.info(average_output)

    return throughput_output,average_output
