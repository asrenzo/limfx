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

from dependency_injector import providers

mqtt_spec = {
        'mqtt_host': 'string(default="127.0.0.1")',
        'mqtt_port': 'integer(default=1883)',
        'mqtt_user': 'string(default="")',
        'mqtt_pwd': 'string(default="")',
        'mqtt_use_ssl': 'boolean(default=False)',
        'mqtt_clean_session': 'boolean(default=True)',
    }


class MqttConf(object):

    def __init__(self, mqtt_host='127.0.0.1', mqtt_port=1883, mqtt_user='', mqtt_pwd='', mqtt_use_ssl=False,
                 mqtt_clean_session=True, userdata=None):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_user = mqtt_user
        self.mqtt_pwd = mqtt_pwd
        self.mqtt_use_ssl = mqtt_use_ssl
        self.mqtt_clean_session = mqtt_clean_session
        self.userdata = userdata


mqtt_configuration = providers.Singleton(MqttConf)