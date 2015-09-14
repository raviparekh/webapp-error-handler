from example_app.error_messages.exceptions import Unauthorised


def validate_user(user_name, passwd):
    # demo user
    if user_name != "user1" or passwd != "pass":
        raise Unauthorised('ERR_001', status_code=403, user=user_name, additional_info={'more_info': 'contact support'})
    # Set session etc
    return True

