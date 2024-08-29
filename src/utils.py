from flask import url_for

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img src='https://github.com/breatheco-de/exercise-family-static-api/blob/master/rigo-baby.jpeg?raw=true' />
        <h1>Hello Rigo!!</h1>
        This is your api home, remember to specify a real endpoint path like: <ul style="text-align: left;">"""+links_html+"</ul></div>"

def validate_payload(payload):
    errors = dict()

    missing_keys = set(["first_name", "age", "lucky_numbers"])
    extra_keys = []

    for key in payload:
        value = payload[key]
        if key == "first_name":
            if not isinstance(value, str):
                errors["first_name"] = "The first name should be a string"
            elif len(value) == 0:
                errors["first_name"] = "The first name should be a non empty string"
            missing_keys.remove("first_name")
        elif key == "age":
            if not isinstance(value, int):
                errors["age"] = "The age should be an integer"
            elif value < 0:
                errors["age"] = "The age should be a non negative integer"
            missing_keys.remove("age")
        elif key == "lucky_numbers":
            if not isinstance(value, list):
                errors["lucky_numbers"] = "Lucky numbers should be a list"
            else:
                # Learned something new :D
                # bool is a subtype of int in Python.
                # See https://stackoverflow.com/a/37888668/9041490
                for e in value:
                    if isinstance(e, bool) or not isinstance(e, int):
                        errors["lucky_numbers"] = "Lucky numbers should be a list of integers"
                        break
            missing_keys.remove("lucky_numbers")
        else:
            extra_keys.append(key)
    
    if len(missing_keys) > 0:
        errors["missing_keys"] = ",".join(missing_keys)

    if len(extra_keys) > 0:
        errors["extra_keys"] = ",".join(extra_keys)

    return (not bool(errors), errors)