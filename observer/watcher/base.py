#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Base Watcher module


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

class Watcher(object):
    def __init__(self, obj, attr, callback):
        if obj.pk is None:
            raise AttributeError(
                    """'%s' instance needs to have primary key before """
                    """observer can watch the instance""" % obj.__class__.__name__)
        self._obj = obj
        self._attr = attr
        self._callback = callback

    def get_attr_value(self):
        """get attribute value"""
        return getattr(self._obj, self._attr)

    def unwatch(self):
        """remove all receivers used in this watcher"""
        raise NotImplementedError

    def call(self):
        """call callback registered in this watcher"""
        self._callback(sender=self, obj=self._obj, attr=self._attr)