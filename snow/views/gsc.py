# coding=utf-8
import flask_login as login
from flask_admin.contrib.sqla import ModelView
from wtforms import fields, validators

from markupsafe import Markup
from snow.ext import db
from snow.models.gsc import Gsc


class GscAdmin(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    @property
    def can_create(self):
        return self.is_accessible() and login.current_user.role

    @property
    def can_edit(self):
        return self.can_create

    @property
    def can_delete(self):
        return self.can_create

    can_view_details = True

    column_labels = {
        'id_': '编号',
        'work_title': '标题',
        'work_author': '作者',
        'work_dynasty': '朝代',
        'foreword': '前言',
        'content': '内容',
        'translation': '翻译',
        'intro': '简介',
        'baidu_wiki': '百度wiki',
        'annotation_': '注释',
        'appreciation': '赏析',
        'master_comment': '辑评',
        'layout': '布局',
        'audio_id': '音频',
    }

    column_sortable_list = ('id_', )

    column_list = (
        'id_', 'work_title', 'work_author', 'layout'
    )
    column_filters = ('id_', 'work_title', 'work_author',
                      'work_dynasty', 'content', 'foreword')

    def _render_baidu_wiki(self, context, model, name):
        if model.baidu_wiki:
            return Markup('<a href="{}" target="_blank">{}</a>'.format(model.baidu_wiki, model.baidu_wiki))

    def _render_audio(self, context, model, name):
        if model.audio_id:
            return Markup('<a href="https://songci.nos-eastchina1.126.net/audio/{}.m4a" '
                          'target="_blank">https://songci.nos-eastchina1.126.net/audio/{}.m4a </a>'.format(model.audio_id, model.audio_id))

    def _render_translation(self, context, model, name):
        if model.translation:
            s = model.translation
            s = s.replace('\n', '<br>')
            return Markup(s)

    def _render_annotation(self, context, model, name):
        if model.annotation_:
            s = model.annotation_
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')

    def _render_content(self, context, model, name):
        if model.content:
            s = model.content
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')

    def _render_foreward(self, context, model, name):
        if model.foreword:
            s = model.foreword
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')

    def _render_master_comment(self, context, model, name):
        if model.master_comment:
            s = model.master_comment
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')

    def _render_appreciation(self, context, model, name):
        if model.appreciation:
            s = model.appreciation
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')

    def _render_intro(self, context, model, name):
        if model.intro:
            s = model.intro
            s = s.replace('\n', '<br>')
            return Markup('<div>' + s + '</div>')
    column_formatters = {
        'baidu_wiki': _render_baidu_wiki,
        'audio_id': _render_audio,
        'translation': _render_translation,
        'annotation_': _render_annotation,
        'content': _render_content,
        'foreward': _render_foreward,
        'master_comment': _render_master_comment,
        'appreciation': _render_appreciation,
        'intro': _render_intro,
    }

    form_extra_fields = {
        'content': fields.TextAreaField(label='内容', default='', validators=[validators.required()]),
        'foreword': fields.TextAreaField(label='前言', default=''),
        'translation': fields.TextAreaField(label='翻译', default=''),
        'intro': fields.TextAreaField(label='简介', default=''),
        'annotation_': fields.TextAreaField(label='注释', default=''),
        'appreciation': fields.TextAreaField(label='赏析', default=''),
        'master_comment': fields.TextAreaField(label='辑评', default=''),
        'audio_id': fields.IntegerField(label='音频id', default=0),
        'layout': fields.SelectField(label='布局', choices=[('indent', '缩进'), ('center', '居中')])
    }

    form_columns = ('work_title', 'work_dynasty', 'work_author', 'foreword', 'content', 'translation', 'intro',
                    'annotation_', 'appreciation', 'master_comment', 'layout', 'baidu_wiki', 'audio_id')

    def on_model_change(self, form, model, is_created=True):
        if is_created:
            with db.session.no_autoflush:
                gsc = Gsc.query.order_by(Gsc.id_.desc()).first()
                model.id_ = gsc.id_ + 1
        return super(GscAdmin, self).on_model_change(form, model, is_created)


category = '条目管理'

gsc_view = GscAdmin(Gsc, db.session, name='诗词列表', category=category)