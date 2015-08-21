# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class ConfigForm(Form):
    roi1ForDrive = BooleanField('roi1', default=False)
    roi2ForDrive = BooleanField('roi2', default=False)
    roi3ForDrive = BooleanField('roi3', default=False)
    roi4ForDrive = BooleanField('roi4', default=False)
    roi5ForDrive = BooleanField('roi5', default=False)
    roi6ForDrive = BooleanField('roi6', default=False)
    roi7ForDrive = BooleanField('roi7', default=False)
    roi8ForDrive = BooleanField('roi8', default=False)
    roi9ForDrive = BooleanField('roi9', default=False)
    roi10ForDrive = BooleanField('roi10', default=False)
    roi11ForDrive = BooleanField('roi11', default=False)
    roi12ForDrive = BooleanField('roi12', default=False)
    roi13ForDrive = BooleanField('roi13', default=False)
    roi14ForDrive = BooleanField('roi14', default=False)
    roi15ForDrive = BooleanField('roi15', default=False)
    roi16ForDrive = BooleanField('roi16', default=False)

    roi1ForLeave = BooleanField('roi1', default=False)
    roi2ForLeave = BooleanField('roi2', default=False)
    roi3ForLeave = BooleanField('roi3', default=False)
    roi4ForLeave = BooleanField('roi4', default=False)
    roi5ForLeave = BooleanField('roi5', default=False)
    roi6ForLeave = BooleanField('roi6', default=False)
    roi7ForLeave = BooleanField('roi7', default=False)
    roi8ForLeave = BooleanField('roi8', default=False)
    roi9ForLeave = BooleanField('roi9', default=False)
    roi10ForLeave = BooleanField('roi10', default=False)
    roi11ForLeave = BooleanField('roi11', default=False)
    roi12ForLeave = BooleanField('roi12', default=False)
    roi13ForLeave = BooleanField('roi13', default=False)
    roi14ForLeave = BooleanField('roi14', default=False)
    roi15ForLeave = BooleanField('roi15', default=False)
    roi16ForLeave = BooleanField('roi16', default=False)
