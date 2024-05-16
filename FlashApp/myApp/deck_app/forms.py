from django.utils import timezone
from django import forms
from deck_app.models import Deck, Card


class FormularioDeck(forms.ModelForm):
    class Meta:
        model = Deck
        exclude = ['usuario', 'erros', 'acertos', 'desempenho_geral', 'criado_em', 'ultima_revisao']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        #self.usuario = kwargs.pop('usuario', None)
        super(FormularioDeck, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormularioCard(forms.ModelForm):
    
    class Meta:
        model = Card
        exclude = []