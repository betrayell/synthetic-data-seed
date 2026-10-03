from datetime import datetime

import data

raw_logs = data.raw_logs

def parsed_logs(raw_logs, parse_logs, corputed_logs, logs_per_services, log_level):

    level_metrics = {
        "INFO": 0,
        "ERROR": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "DEBUG": 0
    }

    service_metrics = {
        "auth-service": 0,
        "payment-service": 0,
        "db-service": 0,
        "api-gateway": 0
    }

    for line in raw_logs:

        errors = []

        is_valid, procces, line, errors = parse_line(line, errors)

        # Log bozuksa
        if not is_valid:
            if line not in corputed_logs:
                corputed_logs.append(line)

            continue

        data = {
            "timestamp": procces[0],
            "log_level": procces[1],
            "service_name": procces[2],
            "message": procces[3]
        }

        # Log level sayacı
        if data.get("log_level") in log_level:
            level_metrics = counter_metrics(
                data,
                level_metrics
            )

        # Service sayacı
        if data.get("service_name") in logs_per_services:
            service_metrics = counter_logs_per_level(
                data,
                service_metrics
            )

        # Geçerli logu listeye ekle
        parse_logs.append(data)

    return (
        True,
        parse_logs,
        corputed_logs,
        level_metrics,
        service_metrics
    )


def parse_line(line, errors):

    result = line.split("|")

    if len(result) != 4:
        errors.append(
            "Log must contain exactly 4 fields."
        )

        return (
            False,
            [],
            line,
            errors
        )

    timestamp, log_level, service_name, message = (
        result[0].strip(),
        result[1].strip(),
        result[2].strip(),
        result[3].strip()
    )

    # Timestamp doğrulaması
    try:
        datetime.datetime.strptime(
    timestamp,
    "%Y-%m-%d %H:%M:%S"
).replace(tzinfo=datetime.timezone.utc)

    except ValueError:
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
        errors.append(
            f"Invalid log level: {log_level}"
        )

    if not service_name or not message:
        errors.append(
            "The service name or message field "
            "cannot be empty."
        )

    processed = [
        timestamp,
        log_level,
        service_name,
        message
    ]

    # Hata varsa geçersiz
    if len(errors) > 0:
        return (
            False,
            processed,
            line,
            errors
        )

    # Hata yoksa geçerli
    return (
        True,
        processed,
        line,
        errors
    )


def counter_metrics(data, logs_per_level):

    level_name = data["log_level"]

    logs_per_level[level_name] = (
        logs_per_level.get(level_name, 0) + 1
    )

    return logs_per_level


def counter_logs_per_level(data, logs_per_service):

    service_name = data["service_name"]

    logs_per_service[service_name] = (
        logs_per_service.get(service_name, 0) + 1
    )

    return logs_per_service


parse_logs = []

corputed_logs = []

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


Bool, parse_logs, corputed_logs, count_metric, count_logs_pers_level = parsed_logs(
    raw_logs,
    parse_logs,
    corputed_logs,
    logs_per_services,
    log_level
)



print("İşlem başarılı:", Bool)

print("\nacceseable logs:")
for log in parse_logs:
    print(log)

print("\ncorrupted logs:")
for log in corputed_logs:
    print(log)

print("\nLog level statistics:")
for level, count in count_metric.items():
    print(f"{level}: {count}")

print("\nService statistics:")
for service, count in count_logs_pers_level.items():
    print(f"{service}: {count}")