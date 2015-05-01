from authority import permissions
import authority


class CrawlContestPermission(permissions.BasePermission):
    label = 'crawl_contest_permission'
    check = ('can_crawl_contest')

    def can_crawl_contest(self):
        # Admin can crawl contest
        return is_admin(self.user)
