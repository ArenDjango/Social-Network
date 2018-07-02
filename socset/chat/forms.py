from django import forms
from .models import *

import os
import unittest

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        exclude = [""]