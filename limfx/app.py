#!/usr/bin/env python
# Encoding: utf-8

#=-
# Copyright (c) 2016, Laurent Rahuel
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of this projet, Laurent Rahuel nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#=-

import gevent
from gevent import monkey
monkey.patch_all()

import os
import sys
import optparse
import textwrap
import StringIO
import logging.config

import configobj
import pkg_resources

from . import config


class Manager(object):
    spec = {
        'mqtt_host': 'string(default="127.0.0.1")',
        'mqtt_port': 'integer(default=1883)',
        'mqtt_user': 'string(default="")',
        'mqtt_pwd': 'string(default="")',
    }

    def __init__(self, mqtt_host='127.0.0.1', mqtt_port=1883, mqtt_user='', mqtt_pwd=''):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_user = mqtt_user
        self.mqtt_pwd = mqtt_pwd

    def start(self):
        msg = 'Manager app launched (mqtt_host : %s, mqtt_port : %s)' %(self.mqtt_host, self.mqtt_port)
        print msg
        logging.getLogger('limfx.manager').info(msg)


class App(object):
    spec = {
        'root': 'string(default="%s")' % pkg_resources.get_distribution('limfx').location,

        'application': {
            '': 'boolean(default=True)',
        },

        'manager': Manager.spec,

        'logging': {
            'formatters': {'keys': 'string(default="")'},
            'handlers': {'keys': 'string(default="")'},
            'loggers': {'keys': 'string(default="root")'},
            'logger_root': {
                'level': 'string(default="NOTSET")',
                'handlers': 'string(default="")'
            }
        }
    }

    def __init__(self, config_file, error, initial_conf=None):
        conf = configobj.ConfigObj(config_file, configspec=configobj.ConfigObj(self.spec), list_values=False, interpolation='Template')
        conf.merge(initial_conf or {})
        config.validate(config_file, conf, error)

        logging.addLevelName(10000, 'NONE')

        log_conf = ''
        for k, v in conf['logging'].items():
            log_conf += '\n[%s]\n' % k
            log_conf += '\n'.join(map('='.join, v.items()))

        logging.config.fileConfig(StringIO.StringIO(log_conf))

        self.manager = Manager(**conf['manager'])


def run(*args, **kw):
    if len(sys.argv) == 1:
        print textwrap.dedent('''
        Usage: %s <command>

        with <command>:
          - start           : launch app
        ''' % os.path.basename(sys.argv[0]))
        return 2

    command = sys.argv.pop(1)
    parser = optparse.OptionParser('%%prog start <config_file>')

    if command == 'start':
        pass
    else:
        parser.error('command not found')

    options, args = parser.parse_args()
    conf = {}

    if len(args) != 1:
        parser.error('<config_file> missing')

    config_file = args[0]
    if not os.path.isfile(config_file):
        parser.error('Configuration file "%s" doesn\'t exist' % config_file)

    # -------------------------------------------------------------------------

    app = App(config_file, parser.error, conf)

    if command == 'start':
        manager = gevent.spawn(app.manager.start)
        manager.join()