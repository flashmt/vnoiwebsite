from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from forum.forms import PostCreateForm, PostUpdateForm
from forum.models import Topic, Forum, ForumGroup, Post


def index(request):
    forum_groups = ForumGroup.objects.all()
    return render(request, 'forum/forum_index.html', {'forum_groups': forum_groups})


def pagination_items(request, items, num_per_page):
    paginator = Paginator(items, num_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def topic_list(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = Topic.objects.filter(forum_id=forum_id)
    topics = pagination_items(request, topics, 2)
    return render(request, "forum/topic_list.html", {'forum': forum,
                                                     'topics': topics})


def topic_retrieve(request, forum_id, topic_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = topic.posts.all()
    return render(request, "forum/topic_retrieve.html", {'forum': forum,
                                                         'topic': topic,
                                                         'post': topic.post,
                                                         'posts': posts})


@login_required
def post_create(request, forum_id=None, topic_id=None, post_id=None, template="forum/post_create.html"):

    topic = forum = post = None

    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
    if post_id:
        post = get_object_or_404(Post, pk=post_id)

    # TODO check permission

    if request.POST:
        # if a request is submitted, handle this request
        form = PostCreateForm(request.POST, user=request.user, forum=forum, topic=topic, parent=post)
        if form.is_valid():
            post = form.save()
            if post.topic_post:
                return HttpResponseRedirect(reverse("forum:topic_retrieve", args=(forum.id, post.topic.id,)))
            else:
                return HttpResponseRedirect('../..')
    else:
        form = PostCreateForm(user=request.user, forum=forum, topic=topic, parent=post)
        return render(request, template, {'form': form, 'forum': forum, 'topic': topic})


@login_required
def post_update(request, forum_id=None, topic_id=None, post_id=None, template="forum/post_update.html"):
    forum = topic = post = None
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        topic = get_object_or_404(Topic, pk=topic_id)
    if post_id:
        post = get_object_or_404(Post, pk=post_id)

    # TODO: check permission

    if request.POST:
        form = PostUpdateForm(instance=post, user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../..')
    else:
        form = PostUpdateForm(instance=post)
        return render(request, template, {'form': form, 'forum': forum, 'topic': topic})


@login_required
def topic_create(request, forum_id=None, template="forum/topic_create.html"):
    return post_create(request, forum_id=forum_id, template=template)
