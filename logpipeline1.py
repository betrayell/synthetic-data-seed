# 📋 LOG PARSER APPLICATION - COMPLETE VERSION
# This script parses, validates, and analyzes log entries from multiple services
# ============================================================================

raw_logs = [
    "2026-08-13 05:40:12 | INFO | auth-service | User 'ozgan' logged in successfully.",
    "2026-08-13 05:41:00 | ERROR | payment-service | Payment failed for order #1092. Reason: Insufficient funds.",
    "2026-08-13 05:41:15 | WARNING | db-service | High query latency detected: 450ms.",
    "2026-08-13 05:42:01 | ERROR | auth-service | Invalid password attempt for user 'admin'.",
    "2026-08-13 05:43:10 | CRITICAL | api-gateway | Rate limit exceeded from IP: 192.168.1.50",
    "Corrupted log line - unrecognizable data",  # ❌ Error: Missing level, service and timestamp info
    "2026-08-13 05:44:00 | DEBUG | auth-service | Token refreshed.",
    "2026-08-13 05:45:12 | ERROR | payment-service | Gateway timeout.",
    "2026-08-13 | INFO | payment-service | Missing time part in timestamp"  # ❌ Error: Incomplete timestamp
]

# ============================================================================
# 🔍 PARSE LINE FUNCTION
# ============================================================================

def parse_line(line, errors):
    """
    🔨 Parses and validates a single log line.
    
    📥 Parameters:
        - line (str): The log line to parse
        - errors (list): List to accumulate validation errors
    
    📤 Returns:
        - Tuple: (is_valid, processed_data, original_line)
          - is_valid (bool): Whether the line passed validation
          - processed_data (list or list): Parsed fields or error messages
          - original_line (str): The original line for reference
    """
    
    # 📍 Step 1: Split the line by pipe delimiter (|)
    result = line.split("|")
    
    # ✅ Validate that exactly 4 columns exist (timestamp | level | service | message)
    if len(result) != 4:
        return (False, ["The number of columns must be 4."], line)

    # 📌 Extract and trim whitespace from each field
    timestamp = result[0].strip()
    log_level = result[1].strip()
    service_name = result[2].strip()
    message = result[3].strip()

    # 🔐 Local error list for this specific line
    line_errors = []
    
    # ============================================================
    # ⏰ VALIDATION 1: Timestamp Format (YYYY-MM-DD HH:MM:SS)
    # ============================================================
    # Expected format has exactly 19 characters with specific positions for separators
    if (len(timestamp) != 19 or 
        timestamp[4] != "-" or timestamp[7] != "-" or 
        timestamp[13] != ":" or timestamp[16] != ":"):
        line_errors.append("❌ Invalid timestamp format (Expected: YYYY-MM-DD HH:MM:SS)")

    # ============================================================
    # 📊 VALIDATION 2: Log Level (Must be one of the valid levels)
    # ============================================================
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level not in valid_levels:
        line_errors.append(f"❌ Invalid log level: {log_level} (Must be one of: {', '.join(valid_levels)})")

    # ============================================================
    # 🛡️ VALIDATION 3: Non-Empty Service Name and Message
    # ============================================================
    if not service_name or not message:
        line_errors.append("❌ The service name or message field cannot be empty.")

    # ============================================================
    # 🎯 DECISION: Return result based on validation
    # ============================================================
    if len(line_errors) > 0:
        # 📋 Accumulate errors in the main errors list
        errors.extend(line_errors)
        return (False, line_errors, line)
        
    # ✨ Return parsed data as a structured list
    return (True, [timestamp, log_level, service_name, message], line)

# ============================================================================
# 📊 MAIN PARSING FUNCTION
# ============================================================================

def parsed_logs(raw_logs):
    """
    🚀 Main function that processes all log lines and generates statistics.
    
    📥 Parameters:
        - raw_logs (list): List of raw log strings to parse
    
    📤 Returns:
        - Tuple: (parsed_logs, corrupted_logs, all_errors, metrics)
          - parsed_logs (list): Successfully parsed log entries
          - corrupted_logs (list): Lines that failed validation
          - all_errors (list): All validation errors encountered
          - metrics (dict): Aggregated statistics
    """
    
    # 📝 Initialize data structures to store results
    parse_logs = []  # ✅ Successfully parsed logs
    corrupted_logs = []  # ❌ Failed validation logs
    errors = []  # 🔴 Error messages
    
    # 📈 Initialize counters for each log level
    logs_per_level = {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }
    
    # 🔧 Initialize counters for each service
    logs_per_service = {
        "auth-service": 0,
        "payment-service": 0,
        "db-service": 0,
        "api-gateway": 0
    }
    
    # ============================================================
    # 🔄 PROCESS EACH LOG LINE
    # ============================================================
    for line in raw_logs:
        # 🔍 Parse and validate the current line
        is_valid, process, original_line = parse_line(line, errors)
        
        # ✅ If the line passed validation
        if is_valid:
            # 📦 Create a structured data dictionary
            data = {
                "timestamp": process[0],
                "log_level": process[1],
                "service_name": process[2],
                "message": process[3]
            }
            
            # 💾 Add to parsed logs list
            parse_logs.append(data)
            
            # 📊 Increment the counter for this log level
            logs_per_level[data["log_level"]] += 1
            
            # 🔧 Increment the counter for this service (if it's a known service)
            if data["service_name"] in logs_per_service:
                logs_per_service[data["service_name"]] += 1
        
        # ❌ If the line failed validation
        else:
            # 🛡️ Add to corrupted logs (avoid duplicates)
            if original_line not in corrupted_logs:
                corrupted_logs.append(original_line)
    
    # ============================================================
    # 📊 COMPILE AGGREGATE METRICS
    # ============================================================
    metrics = {
        "total_processed": len(raw_logs),  # 📈 Total lines processed
        "valid_count": len(parse_logs),  # ✅ Successfully parsed count
        "corrupted_count": len(corrupted_logs),  # ❌ Failed validation count
        "error_count": len(errors),  # 🔴 Total error messages
        "logs_per_level": logs_per_level,  # 📊 Breakdown by log level
        "logs_per_service": logs_per_service  # 🔧 Breakdown by service
    }
    
    # 🎯 Return all results
    return parse_logs, corrupted_logs, errors, metrics

# ============================================================================
# 🎬 EXECUTION AND OUTPUT
# ============================================================================

# 🚀 Call the main parsing function
valid_logs, corrupted_logs, all_errors, metrics = parsed_logs(raw_logs)

# ============================================================================
# 🖥️ DISPLAY RESULTS
# ============================================================================

print("=" * 80)
print("📊 LOG PARSING RESULTS")
print("=" * 80)

# ============================================================
# ✅ Display Valid Logs
# ============================================================
print(f"\n✅ Valid Logs ({metrics['valid_count']}):")
print("-" * 80)
for i, log in enumerate(valid_logs, 1):
    print(f"  [{i}] {log['timestamp']} | {log['log_level']:8} | {log['service_name']:15} | {log['message'][:45]}")

# ============================================================
# ❌ Display Corrupted Logs
# ============================================================
print(f"\n❌ Corrupted Logs ({metrics['corrupted_count']}):")
print("-" * 80)
if corrupted_logs:
    for i, log in enumerate(corrupted_logs, 1):
        print(f"  [{i}] {log}")
else:
    print("  (None - All logs were valid!)")

# ============================================================
# ⚠️ Display Error Messages
# ============================================================
print(f"\n⚠️  Validation Errors ({metrics['error_count']}):")
print("-" * 80)
if all_errors:
    for i, error in enumerate(all_errors, 1):
        print(f"  [{i}] {error}")
else:
    print("  (None - No errors encountered!)")

# ============================================================
# 📈 Display Summary Statistics
# ============================================================
print(f"\n📈 Summary Statistics:")
print("-" * 80)
print(f"  🔢 Total Processed:     {metrics['total_processed']} lines")
print(f"  ✅ Valid:               {metrics['valid_count']} lines ({(metrics['valid_count']/metrics['total_processed']*100):.1f}%)")
print(f"  ❌ Corrupted:           {metrics['corrupted_count']} lines ({(metrics['corrupted_count']/metrics['total_processed']*100):.1f}%)")
print(f"  🔴 Errors Found:        {metrics['error_count']}")

# ============================================================
# 📋 Display Log Level Breakdown
# ============================================================
print(f"\n📋 Logs by Level:")
print("-" * 80)
for level, count in metrics['logs_per_level'].items():
    if count > 0:
        # 🎨 Add emoji based on log level severity
        level_emoji = {
            "DEBUG": "🐛",
            "INFO": "ℹ️ ",
            "WARNING": "⚠️ ",
            "ERROR": "❌",
            "CRITICAL": "🔴"
        }
        emoji = level_emoji.get(level, "•")
        print(f"  {emoji} {level:8} : {count:2} lines")
    
# Print empty message for levels with no logs
levels_with_logs = [level for level, count in metrics['logs_per_level'].items() if count == 0]
if levels_with_logs:
    print(f"  (No logs found for: {', '.join(levels_with_logs)})")

# ============================================================
# 🔧 Display Service Breakdown
# ============================================================
print(f"\n🔧 Logs by Service:")
print("-" * 80)
for service, count in metrics['logs_per_service'].items():
    if count > 0:
        print(f"  🖥️  {service:15} : {count:2} lines")

# Print empty message for services with no logs
services_with_logs = [service for service, count in metrics['logs_per_service'].items() if count == 0]
if services_with_logs:
    print(f"  (No logs found for: {', '.join(services_with_logs)})")

# ============================================================
# 🎯 Final Status
# ============================================================
print("\n" + "=" * 80)
if metrics['corrupted_count'] == 0 and metrics['error_count'] == 0:
    print("✨ SUCCESS: All logs parsed without errors! ✨")
else:
    print(f"⚠️  WARNING: {metrics['corrupted_count']} corrupted logs and {metrics['error_count']} errors found.")
print("=" * 80)