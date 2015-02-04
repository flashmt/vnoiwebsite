from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from forum.forms import PostCreateForm, PostUpdateForm
from forum.models import Topic, Forum, Post


def index(request):
    forums = Forum.objects.all()
    return render(request, 'forum/forum_index.html', {'forums': forums})


def topic_list(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = Topic.objects.filter(forum_id=forum_id)
    return render(request, "forum/topic_list.html", {'forum': forum,
                                                     'topics': topics})


def list(request):
    return HttpResponse("this is list!")


@login_required
def post_create(request, forum_id=None, topic_id=None):

    topic = forum = None

    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        topic_post = False
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum

    #TODO check permission

    if request.POST or request.GET:
        # if a request is submitted, handle this request
        form = PostCreateForm(request.POST, user=request.user, forum=forum, topic=topic)
        if form.is_valid():
            post = form.save()
        # return HttpResponseRedirect(reversed("forum:post_retrieve", args=[post.id]))
        return HttpResponse("Successfully!")
    else:
        form = PostCreateForm()
        return render(request, "forum/post_create.html", {'form': form})


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    #TODO: check permission

    if request.POST or request.GET:
        form = PostUpdateForm(instance=post, user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../')
    else:
        form = PostUpdateForm(instance=post)
        return render(request, "forum/post_update.html", {'form': form})

