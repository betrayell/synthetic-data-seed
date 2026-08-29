def clean_line(line):
        line=line.strip()
        if not line or line.startswith("#"):
            return False
        if "#" in line:  
            line=line.split("#")[0].strip()
        return line

    
def parse_env():
    config={}
    with open("backend.env",mode="r",encoding="utf-8") as file:
        for simple_line in file:
            line=clean_line(simple_line)
            if not line:
                continue
            key,value= cast_value(line)
            if key == None and value == None: continue 
            config[key]=value
    return config
              
        
def cast_value(line):
    True_Bool=["true", "True", "TRUE", "1"]
    False_Bool=["false", "False", "FALSE", "0"]
    if "=" not in line: return None, None
    key,value=line.split("=",1)
    value=value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
    value.startswith("'") and value.endswith("'")):
        value = value.strip("'").strip('"')
    if (key.startswith('"') and key.endswith('"')) or (
    key.startswith("'") and key.endswith("'")):
        key = key.strip("'").strip('"')

    key=key.strip()

    if value in True_Bool:
        return (str(key),True)
    if value in False_Bool:
        return (str(key),False)
    count=value.count(".")
    if  "," in value:
        host_ip_adress = [item.strip() for item in value.split(",")]
        return (str(key),(host_ip_adress))
    if value.isdigit():
        return str(key),int(value)
    if count == 1 and not value.startswith(".") and not value.endswith("."):
       value_control=value.replace(".","")
       if value_control.lstrip("-").isdigit():
             return str(key),float(value)
       
    return (key,value)
  
result=parse_env()
print(result)

