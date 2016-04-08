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

from services.common.configuration import mqtt_spec, mqtt_configuration


class Manager(object):
    def __init__(self, mqtt_conf):
        self.mqtt_conf = mqtt_configuration(**mqtt_conf)

    def _run(self):
        msg = "This is start point"
        #msg = 'Manager app launched (mqtt_host : %s, mqtt_port : %s)' %(self.mqtt_host, self.mqtt_port)
        print msg
        logging.getLogger('limfx.manager').info(msg)

    def run(self):
        me = gevent.spawn(self._run)
        me.join()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))


class App(object):
    spec = {
        'root': 'string(default="%s")' % pkg_resources.get_distribution('limfx').location,

        'application': {
            '': 'boolean(default=True)',
        },

        'mqtt': mqtt_spec,

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

        self.manager = Manager(mqtt_conf=conf['mqtt'])


    def run(self):
        self.manager.run()


def run(*args, **kw):
    if len(sys.argv) == 1:
        print textwrap.dedent('''
        Usage: %s <command>

        with <command>:
          - run           : launch app
        ''' % os.path.basename(sys.argv[0]))
        return 2

    command = sys.argv.pop(1)
    parser = optparse.OptionParser('%%prog start <config_file>')

    if command != 'run':
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

    if command == 'run':
        app.run()