import re


def parse_points(line: str) -> tuple | None:
    """Parse user-provided points

    Return a tuple of 5 values where:
    * the first value is student_id converted to int if it's possible,
    left as a string if not,
    * and remaining 4 values are ints
    """
    line = line.split()
    student_id, *points = line
    if len(points) != 4:
        return None

    try:
        points = [int(p) for p in points]
    except ValueError:
        return None

    for p in points:
        if p < 0:
            return None

    try:
        student_id = int(student_id)
    except ValueError:
        pass

    return student_id, *points


def parse_creds(line: str) -> dict | None:
    """Parse user-provided credentials

    Return credentials in a dict,
    replacing invalid credentials with None.

    Return None if any credentials are missing.
    """
    match = re.match(r'(\S+) (.+) (\S+)', line)
    if not match:
        return None

    first_name, last_name, email = match.groups()
    first_name = re.fullmatch("""
            (?!.*[-']{2})  # No doubles allowed
            (?![-'])  # Not allowed at the beginning
            ([A-Za-z-']{2,})  # First name
            (?<![-'])  # Not allowed at the end
            """, first_name, flags=re.VERBOSE)
    first_name = first_name and first_name.group()

    last_name = re.fullmatch("""
            (?!.*[-']{2})  # No doubles allowed
            (?![-'])  # Not allowed at the beginning
            ([A-Za-z-' ]{2,})  # Last name
            (?<![-'])  # Not allowed at the end
            """, last_name, flags=re.VERBOSE)
    last_name = last_name and last_name.group()

    email = re.fullmatch(r"[-.\w]+@[-.\w]+\.[-.\w]+", email)
    email = email and email.group()

    return {'first name': first_name, 'last name': last_name, 'email': email}
