from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from forum.forms import PostForm, PostCreateForm
from forum.models import Post, Forum, Topic


class PostFormTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        super(PostFormTest, self).setUp()
        self.post_id1 = Post.objects.get(pk=1)

    def test_init(self):
        # Test successful init with instance
        form = PostForm(instance=self.post_id1)
        self.assertTrue(isinstance(form.instance, Post))

        # Test successful init without instance
        form = PostForm(user=User.objects.get(pk=1), forum=Forum.objects.get(pk=1))
        self.assertTrue(isinstance(form.instance, Post))
        self.assertEquals(form.user.id, 1)
        self.assertEquals(form.forum.id, 1)
        self.assertEquals(form.parent, None)

        # Test form.forum and form.topic should be follow form.parent if form.parent != None
        form = PostForm(user=User.objects.get(pk=1), forum=Forum.objects.get(pk=2), topic=Topic.objects.get(pk=2), parent=Post.objects.get(pk=1))
        self.assertEquals(form.topic.id, 1)
        self.assertEquals(form.forum.id, 1)


class PostCreateFormTest(TestCase):

    fixtures = ['forum.json', 'auth.json']

    def setUp(self):
        super(PostCreateFormTest, self).setUp()
        self.post_id1 = Post.objects.get(pk=1)

    def test_init(self):
        # Test 'tile' field should be display is the post is a topic post
        form = PostCreateForm(forum=Forum.objects.get(pk=1))
        self.assertEquals(form.forum.id, 1)
        self.assertTrue(form.fields['title'].required)
        self.assertEquals(form.fields['title'].widget.__class__, forms.TextInput().__class__)
        # Test 'title' field should be hidden if the post is not a topic post
        form = PostCreateForm(topic=Topic.objects.get(pk=1))
        self.assertEquals(form.topic.id, 1)
        self.assertFalse(form.fields['title'].required)
        self.assertEquals(form.fields['title'].widget.__class__, forms.HiddenInput().__class__)

                 
    def test_save(self):
        # Test if commit=False, no actual database updating
        pass
        # Test if this post create new topic, a corresponding topic should be created
        pass
        # Test if this post doesn't create new topic, post attributes should be set properly
        pass

    def test_valid_form(self):
        pass

    def test_invalid_form(self):
        # Test form invalid if any required field is empty
        pass


class PostUpdateFormTest(TestCase):

    def test_init(self):
        pass

    def test_save(self):
        pass

    def test_valid_form(self):
        pass

    def test_invalid_form(self):
        pass
