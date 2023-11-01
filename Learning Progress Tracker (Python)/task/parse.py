import re


def parse_points(line: str) -> tuple[int, ...] | None:
    line = line.split()
    if len(line) == 5:
        student_id, *points = line
        try:
            points = [int(p) for p in points]
        except ValueError:
            return None

        try:
            student_id = int(student_id)
        except ValueError:
            pass

        for p in points:
            if p < 0:
                return None

        return student_id, *points
    else:
        return None


def parse_creds(line: str) -> dict | None:
    """Parse user-provided credentials

    Return a Creds object with credentials as attributes,
    replacing invalid credentials with None.

    Return None if any credentials are missing.
    """
    match = re.match(r'(\S+) (.+) (\S+)', line)
    if match:
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

        return dict(first_name=first_name, last_name=last_name, email=email)
    else:
        return None
