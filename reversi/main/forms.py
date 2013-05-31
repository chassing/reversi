
 # coding=utf-8

from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput
from bootstrap_toolkit.widgets import create_prepend_append

from registration.forms import RegistrationForm as RegistrationFormOrig

from django.template.defaultfilters import mark_safe

from models import ReversiUser
from models import CELL_PLAYER1, CELL_PLAYER2

from utils import random_game_name


class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.bootstrap, kwargs = create_prepend_append(**kwargs)
        super(BootstrapSelect, self).__init__(*args, **kwargs)


class RegistrationForm(RegistrationFormOrig):
    nickname = forms.CharField(
        label="Spitzname",
        max_length=254,
        help_text=u'Der Spitznamen kann jederzeit unter den Profileinstellungen geändert werden.',
    )


class MultiplayerGameForm(forms.Form):
    name = forms.CharField(
        label=mark_safe('<span class="text-large">Spielname</span>'),
        initial=random_game_name,
        max_length=100,
        help_text=u'Jede Schlacht sollte einen sehr coolen Namen für die Geschichtsbücher haben!',
        widget=BootstrapTextInput(
            prepend='N',
            attrs={
                'placeholder': 'Benenne das Spiel',
                'class': 'input-xxlarge'
            }
        ),
    )
    player = forms.ChoiceField(
        label=mark_safe(u'<span class="text-large">Wer beginnt die Schlacht?</span>'),
        help_text=u"Wähle ob Du die legendäre Schlacht beginnen oder Dein Territorium verteiltigen möchstest.",
        choices=(
            (CELL_PLAYER1, "Ich selbst"),
            (CELL_PLAYER2, "Mein Gegner"),
        ),
        widget=forms.RadioSelect(
            attrs={
                'inline': True,
                'class': 'input-xlarge'
            }
        )
    )
    color = forms.ChoiceField()

    def __init__(self, user, *args, **kwargs):
        super(MultiplayerGameForm, self).__init__(*args, **kwargs)
        self.fields["color"] = forms.ChoiceField(
            label=mark_safe('<span class="text-large">Meine Farbe</span>'),
            choices=(
                (CELL_PLAYER1, user.theme.player1),
                (CELL_PLAYER2, user.theme.player2),
            ),
            widget=forms.RadioSelect(
                attrs={
                    'inline': True,
                    'class': 'input-xlarge'
                }
            )
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ReversiUser
        fields = ('nickname', 'email', 'theme')
        widgets = {
            'nickname': BootstrapTextInput(
                prepend='N',
            ),
            'email': BootstrapTextInput(
                prepend='E',
            ),
        }
