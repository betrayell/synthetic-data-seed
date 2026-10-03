import data


def parsed_logs(raw_logs):
    parse_logs = []
    corrupted_logs = []
    logs_per_level = {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    logs_per_service = {"auth-service": 0, "payment-service": 0, "db-service": 0, "api-gateway": 0}
    errors = []
    
    for line in raw_logs:
        is_valid, process, _ = parse_line(line)
        
        if is_valid:
            data = {
                "timestamp": process[0],
                "log_level": process[1],
                "service_name": process[2],
                "message": process[3]
            }
            parse_logs.append(data)
            logs_per_level[data["log_level"]] += 1
            if data["service_name"] in logs_per_service:
                logs_per_service[data["service_name"]] += 1
        else:
            if line not in corrupted_logs:
                corrupted_logs.append(line)
            errors.extend(process)  # process = error list
    
    return {
        "parsed": parse_logs,
        "corrupted": corrupted_logs,
        "errors": errors,
        "metrics": {
            "per_level": logs_per_level,
            "per_service": logs_per_service
        }
    }


def parse_line(line):
    result = line.split("|")
    if len(result) != 4:
        return (False, ["Column count must be 4"], line)
    
    timestamp, log_level, service_name, message = [x.strip() for x in result]
    
    line_errors = []
    
    if len(timestamp) != 19 or timestamp[4] != "-" or timestamp[7] != "-" or timestamp[13] != ":" or timestamp[16] != ":":
        line_errors.append("Invalid timestamp format")
    
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level not in valid_levels:
        line_errors.append(f"Invalid log level: {log_level}")
    
    if not service_name or not message:
        line_errors.append("Empty service name or message")
    
    if line_errors:
        return (False, line_errors, line)
    
    return (True, [timestamp, log_level, service_name, message], line)

result = parsed_logs(data.raw_logs)
print(f"Valid: {len(result['parsed'])}")
print(f"Corrupted: {len(result['corrupted'])}")
print(f"Errors: {len(result['errors'])}")
print(f"Levels: {result['metrics']['per_level']}")
print(f"Services: {result['metrics']['per_service']}")

