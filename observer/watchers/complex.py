#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Complex watcher module


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.db.models import Model

from base import Watcher
from value import ValueWatcher
from model import ModelWatcher
from relation import RelatedManagerWatcher
from relation import ManyRelatedManagerWatcher

RelatedManagerTypeName = "<class 'django.db.models.fields.related.RelatedManager'>"
ManyRelatedManagerTypeName = "<class 'django.db.models.fields.related.ManyRelatedManager'>"

class ComplexWatcher(Watcher):
    """Watch any field as you think

    Watch Value/Model/Relation field. If the field is...

    Value:
        Simply watch the modification of the field

    Model (ForeignKey):
        Watch the field modification and the model instance modification.
        If you modify the related instance of field, callback is called.

    Relatin (ForeignKey[reverse], ManyToManyField):
        Watch the field modification (add, remove, clear) and each related model
        instance modification. If you modify the related instance of collection,
        callback is called.

    If you want to customize the behavior of watcher, use this class for superclass
    """
    def __init__(self, obj, attr, callback):
        super(ComplexWatcher, self).__init__(obj, attr, callback)

        attr_value = self.get_attr_value()

        self._value_watcher = None
        self._model_watcher = None
        self._model_watchers = []
        self._related_manager_watcher = None
        self._many_related_manager_watcher = None

        if isinstance(attr_value, Model):
            self._set_value_watcher()
            self._set_model_watcher()
        elif str(type(attr_value)) == RelatedManagerTypeName:
            self._set_related_manager_watcher()
            self._set_model_watchers()
        elif str(type(attr_value)) == ManyRelatedManagerTypeName:
            self._set_many_related_manager_watcher()
            self._set_model_watchers()
        else:
            self._set_value_watcher()

    def unwatch(self):
        self._delete_watcher('_value_watcher')
        self._delete_watcher('_model_watcher')
        self._delete_watcher('_model_watchers')
        self._delete_watcher('_related_manager_watcher')
        self._delete_watcher('_many_related_manager_watcher')

    def _delete_watcher(self, name):
        if name == '_model_watchers':
            if self._model_watchers != []:
                for model_watcher in self._model_watchers:
                    model_watcher.unwatch()
            self._model_watchers = []
        else:
            watcher = getattr(self, name, None)
            if watcher:
                watcher.unwatch()
                setattr(self, name, None)

    def _set_value_watcher(self):
        self._delete_watcher('_value_watcher')
        self._value_watcher = ValueWatcher(self._obj, self._attr, self._value_watcher_callback)
    def _set_model_watcher(self):
        self._delete_watcher('_model_watcher')
        self._model_watcher = ModelWatcher(self.get_attr_value(), None, self._model_watcher_callback)
    def _set_model_watchers(self):
        self._delete_watcher('_model_watchers')
        for model in self.get_attr_value().iterator():
            self._model_watchers.append(ModelWatcher(model, None, self._model_watcher_callback))
    def _set_related_manager_watcher(self):
        self._delete_watcher('_related_manager_watcher')
        self._related_manager_watcher = RelatedManagerWatcher(self._obj, self._attr, self._related_manager_watcher_callback)
    def _set_many_related_manager_watcher(self):
        self._delete_watcher('_many_related_manager_watcher')
        self._many_related_manager_watcher = ManyRelatedManagerWatcher(self._obj, self._attr, self._many_related_manager_watcher_callback)

    def _value_watcher_callback(self, sender, obj, attr):
        self.call()
        if self._model_watcher:
            self._set_model_watcher()

    def _model_watcher_callback(self, sender, obj, attr):
        self.call()

    def _related_manager_watcher_callback(self, sender, obj, attr):
        self.call()
        self._set_model_watchers()
        
    def _many_related_manager_watcher_callback(self, sender, obj, attr):
        self.call()
        self._set_model_watchers()