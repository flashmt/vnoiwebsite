import authority
from authority import permissions
from contests.models import ContestStandingTable

# Assume all user must be authenticated before check this permission
from vnoiusers.user_util import is_admin


class ContestPermission(permissions.BasePermission):
    label = 'contest_permission'
    check = 'can_crawl_contest'

    def can_crawl_contest(self):
        # Admin can crawl contest
        return is_admin(self.user)


authority.register(ContestStandingTable, ContestPermission)
