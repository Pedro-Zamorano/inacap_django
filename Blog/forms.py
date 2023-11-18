from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Titulo',
                            max_length=255,
                            required=True,
                            widget=forms.TextInput(attrs={
                                'class': "form-control",
                                'placeholder': 'Titulo de tu post'
                                }))
    content = forms.CharField(label='Contenido',
                            required=True, 
                            widget=forms.Textarea(attrs={
                                'class': "form-control",
                                'placeholder': 'Escribe tu post'
                                }))

    class Meta:
        model = Post
        fields = ('title', 'content',)