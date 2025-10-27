from django import forms
from .models import Item, Comment, Claim
from django.contrib.auth.forms import AuthenticationForm

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label='School ID')
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'location', 'date_lost', 'contact_info']  
        # Add all fields you want editable

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ClaimForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label='Message')

    class Meta:
        model = Claim
        fields = ['message']
