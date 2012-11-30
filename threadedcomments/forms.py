from django import forms
from django.contrib.comments.forms import CommentForm
from django.conf import settings
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from threadedcomments.models import ThreadedComment

class ThreadedCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(ThreadedCommentForm, self).__init__(target_object, data=data,
            initial=initial)

        if 'name' in self.fields:
            del self.fields['name']
        if 'email' in self.fields:
            del self.fields['email']
        if 'url' in self.fields:
            del self.fields['url']

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        self.cleaned_data['name'] = ''
        self.cleaned_data['url'] = ''
        self.cleaned_data['email'] = ''
        d = super(ThreadedCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        return d
