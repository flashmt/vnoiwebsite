from authority import permissions
import authority
from forum.models import Forum, Vote, Post, Topic

# Assume all user must be authenticated before check this permission
from vnoiusers.user_util import is_admin


class ForumPermission(permissions.BasePermission):
    label = 'forum_permission'
    checks = ('can_create_forum', 'can_update_forum')

    def can_create_forum(self):
        # Admin can create a forum
        return is_admin(self.user)

    def can_update_forum(self, forum):
        # Admin can update forum
        return is_admin(self.user)


class PostPermission(permissions.BasePermission):

    label = 'post_permission'
    checks = ('can_create_post', 'can_update_post', 'can_delete_post')

    def can_create_post(self):
        # Authenticated User can create post
        return True

    def can_update_post(self, post):
        # Admin can update post
        if is_admin(self.user):
            return True
        # Author can update post
        if self.user == post.created_by:
            return True
        return False

    def can_delete_post(self, post):
        # Admin can delete post
        return is_admin(self.user)


class TopicPermission(PostPermission):

    label = 'topic_permission'
    checks = 'can_toggle_pin'

    def can_toggle_pin(self):
        # Only admin can pin topic
        return is_admin(self.user)


class VotePermission(permissions.BasePermission):
    label = 'vote_permission'
    checks = ('can_create_vote', )

    def can_create_vote(self, post):
        # Authenticated user can create vote
        return True


authority.register(Forum, ForumPermission)
authority.register(Vote, VotePermission)
authority.register(Post, PostPermission)
authority.register(Topic, TopicPermission)

