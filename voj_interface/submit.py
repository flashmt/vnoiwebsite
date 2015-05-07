def voj_submit(user, code, language):
    # TODO
    # To avoid the user from waiting too long (submit to VOJ can take time)
    # Fork a new thread to submit using Celery:
    #     http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
    # This thread will be responsible for sending HTTP request to VOJ.
    # After we finished creating this thread, return and let Django return HTTP response
    # to user
    pass
