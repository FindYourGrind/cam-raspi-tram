# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class ConfigForm(Form):
    roi1ForDrive = BooleanField('roi1', id='droi1', default=False)
    roi2ForDrive = BooleanField('roi2', id='droi2', default=False)
    roi3ForDrive = BooleanField('roi3', id='droi3', default=False)
    roi4ForDrive = BooleanField('roi4', id='droi4', default=False)
    roi5ForDrive = BooleanField('roi5', id='droi5', default=False)
    roi6ForDrive = BooleanField('roi6', id='droi6', default=False)
    roi7ForDrive = BooleanField('roi7', id='droi7', default=False)
    roi8ForDrive = BooleanField('roi8', id='droi8', default=False)
    roi9ForDrive = BooleanField('roi9', id='droi9', default=False)
    roi10ForDrive = BooleanField('roi10', id='droi10', default=False)
    roi11ForDrive = BooleanField('roi11', id='droi11', default=False)
    roi12ForDrive = BooleanField('roi12', id='droi12', default=False)
    roi13ForDrive = BooleanField('roi13', id='droi13', default=False)
    roi14ForDrive = BooleanField('roi14', id='droi14', default=False)
    roi15ForDrive = BooleanField('roi15', id='droi15', default=False)
    roi16ForDrive = BooleanField('roi16', id='droi16', default=False)

    roi1ForLeave = BooleanField('roi1', id='lroi1', default=False)
    roi2ForLeave = BooleanField('roi2', id='lroi2', default=False)
    roi3ForLeave = BooleanField('roi3', id='lroi3', default=False)
    roi4ForLeave = BooleanField('roi4', id='lroi4', default=False)
    roi5ForLeave = BooleanField('roi5', id='lroi5', default=False)
    roi6ForLeave = BooleanField('roi6', id='lroi6', default=False)
    roi7ForLeave = BooleanField('roi7', id='lroi7', default=False)
    roi8ForLeave = BooleanField('roi8', id='lroi8', default=False)
    roi9ForLeave = BooleanField('roi9', id='lroi9', default=False)
    roi10ForLeave = BooleanField('roi10', id='lroi10', default=False)
    roi11ForLeave = BooleanField('roi11', id='lroi11', default=False)
    roi12ForLeave = BooleanField('roi12', id='lroi12', default=False)
    roi13ForLeave = BooleanField('roi13', id='lroi13', default=False)
    roi14ForLeave = BooleanField('roi14', id='lroi14', default=False)
    roi15ForLeave = BooleanField('roi15', id='lroi15', default=False)
    roi16ForLeave = BooleanField('roi16', id='lroi16', default=False)
