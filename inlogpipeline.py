information=[
     {"name":"ahmet","surname":"yilmaz","age":25,"mail":"ahmetyilmazgmail.com"},
     {"name":"mehmet","surname":"eryil","age":30,"mail":"mehmeteryilhotmail.com"},
     {"name":"ayse","surname":"demir","age":28,"mail":"aysedemirgmail"} ,
     {"name":"","surname":"kaya","age":22,"mail":"atillakaya@hotmail.com"},
     {"surname":"taskin","age":27,"mail":1213},
     {"name":"ali","surname":"kaya","age":34,"mail":"@hotmail.com"},
     {"name":"veli","surname":"demir","age":30,"mail":""},
     {"name":"kemal","surname":"kaya","age":22,"mail":".com"},
     {"name":"atilla","surname":"kaya","age":45,"mail":"atillakaya@hotmail.com"},
     {"name":"atilla","surname":"kaya","age":45,"mail":"atillakaya@hotmail.com"},
     {"name":"","surname":"kaya","age":17,"mail":"atillakaya@hotmail.com"},
     {"name":"muhammet","surname":"yildirim","age":"Aas","mail":"muhammetyilmaz@hotmail.com"},
     {"name":"emir","surname":0,"age":29,"mail":"emiryuksekgmail.com"},
     {"name":"emir","surname":None,"age":21,"mail":"emiryuksekgmail.com"},
     {"name":"hafiz","surname":"kisa","age":20,"mail":""},
     {"name":"muzaffer","surname":"parmak","age":21,"mail":"muzafferparmak@gmail.com"},
     {"":"efe","surname":"sert","age":65,"mail":"efesert@gmail.com"}
]
def validate_information(info):
    succets=[]
    fails=[]
    for item in info:
        is_valid , error_reason = controller(item)
        if is_valid:
             if not item in succets:
               succets.append(item)

        else:
             fails.append({"data": item, "error_reason": error_reason})
           
    return (succets,fails)
    


def controller(items: dict):
    errors = [] 

    required_keys = ["name", "surname", "age", "mail"]
    for key in required_keys:
        if key not in items:
            errors.append(f"The '{key}' key does not exist.")

    if "name" in items:
        name = items.get("name")
        if not isinstance(name, str) or len(name.strip()) < 3:
            errors.append("Name must be a string with at least 3 characters.")

    if "surname" in items:
        surname = items.get("surname")
        if not isinstance(surname, str) or len(surname.strip()) < 3:
            errors.append("Surname must be a string with at least 3 characters.")

    if "age" in items or  isinstance(age, bool):
        age = items.get("age")
        if not isinstance(age, int):
            errors.append("Age must be an integer.")
        elif age < 18:
            errors.append("Age must be 18 or older.")

    if "mail" in items:
        email = items.get("mail")
        if not isinstance(email, str):
            errors.append("Mail must be a string.")
        else:
            if "@" not in email or "." not in email:
                errors.append("Mail must contain '@' and '.'")
            if email.startswith("@") or email.endswith("@") or email.startswith(".") or email.endswith("."):
                errors.append("Invalid email structure.")


    if len(errors) > 0:
        return (False, errors) 
    
    return (True, None)
          
         
succets,fails=validate_information(information)
print("The succets")
print(succets)
print("The fails")
print(fails)














        
            



