from time import sleep
from voj_interface.const import MAX_CRAWLABLE_STATUS_PAGE, VOJ_STATUS_SLEEP_TIME


def crawl_status_page():
    for page_id in xrange(MAX_CRAWLABLE_STATUS_PAGE):
        crawl_status_page_single(page_id)


def crawl_status_page_single(page_id):
    # Crawl a single status page
    URL = 'http://vn.spoj.com/status/start={}'.format(page_id * 20)

    # Get HTML and retrieve all submissions:
    # - Submission ID
    # - VOJ account
    # - Result
    # When result == judged --> we can update it:
    # - Update pending submission (for each user, as well as all pending submissions)
    #     - We must figure out how to store these values efficiently, since it will be
    #       updated very frequently
    #     - If we store in DB --> maybe too slow
    #     - If we store in DB + cache --> how to invalidate cache? and also the value may
    #       change too frequently
    #     - Store in memory --> how to scale the app? (if we have multiple app, how to
    #       share this variables through all instances of app?) --> have separate process
    #       for storing this value?
    # - We must also update pending_submissions array (see main below)
    # - Update the submission_status and submission_verdict in DB
    pass


def crawl_status_page_user(username):
    URL = 'http://vn.spoj.com/status/{}'.format(username)
    pass


def main():
    # This is the method to be called
    # First, retrieve the list of all pending submissions
    pending_submissions = []

    # First, we must crawl status page
    crawl_status_page()

    # If any pending_submissions is not updated, it means that the submission disappeared
    # from status page
    # --> we must crawl this submission from user status page
    for pending_submission in pending_submissions:
        crawl_status_page_user('user_name')

    sleep(VOJ_STATUS_SLEEP_TIME)
