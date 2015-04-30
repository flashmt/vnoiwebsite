# -*- encoding: utf-8 -*-

from datetime import datetime
from django import forms
from forum.models import Post, Topic
from django.utils.html import escape


class PostForm(forms.ModelForm):

    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'size': '80'}))

    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.topic = kwargs.pop('topic', None)
        self.forum = kwargs.pop('forum', None)
        self.parent = kwargs.pop('parent', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if self.parent:
            self.topic = self.parent.topic
            self.forum = self.parent.topic.forum
        self.fields.keyOrder = [
            'title', 'content',
        ]


class PostCreateForm(PostForm):

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = u'Chủ đề'
        self.fields['content'].label = u'Nội dung'
        if self.topic:
            # If this post is not a topic post, title is not required
            self.fields['title'].required = False
            self.fields['title'].widget = forms.HiddenInput()

    def save(self, commit=True):
        if not self.topic:
            # if this post create new topic, create this corresponding topic
            topic = Topic(forum=self.forum,
                          title=escape(self.cleaned_data['title']),
                          created_by=self.user,
                          updated_by=self.user)
            topic.save()
            self.topic = topic
            topic_post = True
        else:
            topic = self.topic
            topic_post = False

        post = Post(topic=topic,
                    created_by=self.user,
                    updated_by=self.user,
                    topic_post=topic_post,
                    content=self.cleaned_data['content'],
                    reply_on=self.parent)
        post.topic = topic
        if commit:
            post.save()
            if topic_post:
                topic.post = post
                topic.content = post.content
                topic.save()

        return post


class PostFormNoParent(PostCreateForm):

    def __init__(self, *args, **kwargs):
        super(PostFormNoParent, self).__init__(*args, **kwargs)
        self.fields['parent'] = forms.IntegerField()
        self.fields['parent'].widget = forms.HiddenInput()

        def tmp():
            pass
        self.fields['parent'].str = tmp


class PostUpdateForm(PostForm):
    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.initial['title'] = self.instance.topic.title
        if not self.instance.topic_post:
            self.fields['title'].required = False
            self.fields['title'].widget = forms.HiddenInput()

    def save(self, commit=True):
        post = self.instance
        post.updated_at = datetime.now()
        if commit:
            post.save()
        if post.topic_post:
            # Update corresponding topic
            topic = post.topic
            topic.content = post.content
            topic.title = escape(self.cleaned_data['title'])
            topic.save()

        return post
