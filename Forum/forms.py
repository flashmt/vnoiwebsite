from django import forms
from forum.models import Post, Topic


class PostForm(forms.ModelForm):

    class Meta:
        model = Post


class PostCreateForm(PostForm):

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        if self.topic:
            self.field['title'].require = False

    def save(self):
        topic_post = False
        if not self.topic:
            # if this post create new topic, create this corresponding topic
            topic = Topic(forum=self.forum,
                          created_by=self.user,
                          title=self.cleaned_data['title'],)
            topic_post = True
            topic.save()
        else:
            topic = self.topic

        post = Post(topic=topic,
                    created_by=self.user,
                    content=self.cleaned_data['content'],
                    topic_post=topic_post)
        return post


    class Meta:
        model = Post

