import data


def parsed_logs(raw_logs, parse_logs, corrupted_logs, logs_per_services, log_level, metrics):

    for line in raw_logs:
        errors = []

        is_valid, process, line = parse_line(line, errors)

        if is_valid:

            data = {
                "timestamp": process[0],
                "log_level": process[1],
                "service_name": process[2],
                "message": process[3]
            }

            parse_logs.append(data)

            metrics["total_processed"] += 1
            metrics["valid_count"] += 1

            if data.get("log_level") in log_level:
                count = counter_metrics(data, metrics)
            else:
                count = 0

            if data.get("service_name") in logs_per_services:
                count = counter_logs_per_level(data, metrics)

            # Critical sayısı
            if data.get("log_level") == "CRITICAL":
                metrics["critical_errors_count"] += 1

        else:

            metrics["total_processed"] += 1
            metrics["corrupted_count"] += 1

            if line not in corrupted_logs:
                corrupted_logs.append(line)

            count = 0

    return (True, parse_logs, corrupted_logs, metrics,count)


def parse_line(line, errors):

    result = line.split("|")

    if len(result) != 4:
        return (False, ["The number of columns must be 4."], line)

    timestamp, log_level, service_name, message = (
        result[0].strip(),
        result[1].strip(),
        result[2].strip(),
        result[3].strip()
    )

    if (len(timestamp) != 19 or
            timestamp[4] != "-" or
            timestamp[7] != "-" or
            timestamp[13] != ":" or
            timestamp[16] != ":"):

        errors.append(
            "Invalid timestamp format "
            "(Expected: YYYY-MM-DD HH:MM:SS)"
        )

    valid_levels = [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ]

    if log_level not in valid_levels:
        errors.append(f"Invalid log level: {log_level}")

    if not service_name or not message:
        errors.append(
            "The service name or message field cannot be empty."
        )

    if len(errors) > 0:
        return (False, errors, line)

    return (
        True,
        [timestamp, log_level, service_name, message],
        line
    )


def counter_metrics(data, metrics):

    level_name = data["log_level"]

    metrics["logs_per_level"][level_name] = (
        metrics["logs_per_level"].get(level_name, 0) + 1
    )

    return metrics["logs_per_level"][level_name]


def counter_logs_per_level(data, metrics):

    service_name = data["service_name"]

    metrics["logs_per_service"][service_name] = (
        metrics["logs_per_service"].get(service_name, 0) + 1
    )

    return metrics["logs_per_service"][service_name]


parse_logs = []
corrupted_logs = []

log_level = [
    "INFO",
    "ERROR",
    "WARNING",
    "CRITICAL",
    "DEBUG"
]

logs_per_services = [
    "auth-service",
    "payment-service",
    "db-service",
    "api-gateway"
]


metrics = {
    "total_processed": 0,
    "valid_count": 0,
    "corrupted_count": 0,
    "critical_errors_count": 0,

    "logs_per_level": {
        "INFO": 0,
        "ERROR": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "DEBUG": 0
    },

    "logs_per_service": {
        "auth-service": 0,
        "payment-service": 0,
        "db-service": 0,
        "api-gateway": 0
    }
}


result = parsed_logs(
    data.raw_logs,
    parse_logs,
    corrupted_logs,
    logs_per_services,
    log_level,
    metrics
)

_, parse_logs, corrupted_logs, metrics, count = result



print("PARSED LOGS:")
print(parse_logs)

print("\nCORRUPTED LOGS:")
print(corrupted_logs)

print("\nMETRICS:")
print(metrics)
print("\nCount:", count)