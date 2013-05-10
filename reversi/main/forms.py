
 # coding=utf-8

from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput
from bootstrap_toolkit.widgets import create_prepend_append

from registration.forms import RegistrationForm as RegistrationFormOrig


from models import ReversiUser
from models import CELL_PLAYER1, CELL_PLAYER2

from utils import random_game_name


class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.bootstrap, kwargs = create_prepend_append(**kwargs)
        super(BootstrapSelect, self).__init__(*args, **kwargs)


class RegistrationForm(RegistrationFormOrig):
    nickname = forms.CharField(
        max_length=254,
        help_text=u'Der Spitznamen kann jederzeit unter den Profileinstellungen geändert werden.',
    )


class MultiplayerGameForm(forms.Form):
    name = forms.CharField(
        initial=random_game_name,
        max_length=100,
        help_text=u'Jeder Schlacht sollte einen sehr coolen Namen für die Geschichtsbücher haben!',
        widget=BootstrapTextInput(
            prepend='N',
            attrs={
                'placeholder': 'Benenne das Spiel',
                'class': 'input-xlarge'
            }
        ),
    )
    player1 = forms.ModelChoiceField(
        label="SpielerIn 1",
        queryset=ReversiUser.objects.all(),
        help_text=u'Der/Die erste SpielerIn fängt die legendäre Schlacht an.',
        widget=BootstrapSelect(
            prepend='P1',
            attrs={
                'class': 'input-xlarge'
            }
        ),
    )
    color_player1 = forms.ChoiceField()
    player2 = forms.ModelChoiceField(
        label="SpielerIn 2",
        queryset=ReversiUser.objects.all(),
        help_text=u'Der/Die zweite SpielerIn verteitigt am Anfang und wird später siegreich sein.',
        widget=BootstrapSelect(
            prepend='P2',
            attrs={
                'class': 'input-xlarge'
            }
        ),
    )
    color_player2 = forms.ChoiceField()

    def __init__(self, user, *args, **kwargs):
        super(MultiplayerGameForm, self).__init__(*args, **kwargs)
        self.fields["color_player1"] = forms.ChoiceField(
            label="Farbe SpielerIn 1",
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
        self.fields["color_player2"] = forms.ChoiceField(
            label="Farbe SpielerIn 2",
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

    def clean(self):
        cleaned_data = super(MultiplayerGameForm, self).clean()
        # different players choosen
        player1 = cleaned_data.get("player1")
        player2 = cleaned_data.get("player2")
        if player1 == player2:
            raise forms.ValidationError("Du kannst nicht gegen dich selbst spielen!")
        # different colors choosen
        color_player1 = cleaned_data.get("color_player1")
        color_player2 = cleaned_data.get("color_player2")
        if color_player1 == color_player2:
            raise forms.ValidationError("Die Spieler dürfen nicht die gleiche Farbe haben!")

        return cleaned_data


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
