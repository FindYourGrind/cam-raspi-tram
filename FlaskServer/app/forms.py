# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

class ConfigForm(Form):
    roi1ForDrive = BooleanField('droi1', default=False)
    roi2ForDrive = BooleanField('droi2', default=False)
    roi3ForDrive = BooleanField('droi3', default=False)
    roi4ForDrive = BooleanField('droi4', default=False)
    roi5ForDrive = BooleanField('droi5', default=False)
    roi6ForDrive = BooleanField('droi6', default=False)
    roi7ForDrive = BooleanField('droi7', default=False)
    roi8ForDrive = BooleanField('droi8', default=False)
    roi9ForDrive = BooleanField('droi9', default=False)
    roi10ForDrive = BooleanField('droi10', default=False)
    roi11ForDrive = BooleanField('droi11', default=False)
    roi12ForDrive = BooleanField('droi12', default=False)
    roi13ForDrive = BooleanField('droi13', default=False)
    roi14ForDrive = BooleanField('droi14', default=False)
    roi15ForDrive = BooleanField('droi15', default=False)
    roi16ForDrive = BooleanField('droi16', default=False)

    roi1ForLeave = BooleanField('lroi1', default=False)
    roi2ForLeave = BooleanField('lroi2', default=False)
    roi3ForLeave = BooleanField('lroi3', default=False)
    roi4ForLeave = BooleanField('lroi4', default=False)
    roi5ForLeave = BooleanField('lroi5', default=False)
    roi6ForLeave = BooleanField('lroi6', default=False)
    roi7ForLeave = BooleanField('lroi7', default=False)
    roi8ForLeave = BooleanField('lroi8', default=False)
    roi9ForLeave = BooleanField('lroi9', default=False)
    roi10ForLeave = BooleanField('lroi10', default=False)
    roi11ForLeave = BooleanField('lroi11', default=False)
    roi12ForLeave = BooleanField('lroi12', default=False)
    roi13ForLeave = BooleanField('lroi13', default=False)
    roi14ForLeave = BooleanField('lroi14', default=False)
    roi15ForLeave = BooleanField('lroi15', default=False)
    roi16ForLeave = BooleanField('lroi16', default=False)
