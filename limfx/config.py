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

"""Helper to validate a configuration"""

import configobj
from validate import Validator


def _validate(filename, config):
    """Validate a ``ConfigObj`` object

    In:
      -  ``filename`` -- the path to the configuration file
      - ``config`` -- the ``ConfigObj`` object, created from the configuration file

    Return:
      - yield the error messages
    """
    errors = configobj.flatten_errors(config, config.validate(Validator(), preserve_errors=True))

    for sections, name, error in errors:
        yield 'file "%s", section "[%s]", parameter "%s": %s' % (filename, ' / '.join(sections), name, error)


def validate(filename, config, error):
    """Validate a ``ConfigObj`` object

    In:
      -  ``filename`` -- the path to the configuration file
      - ``config`` -- the ``ConfigObj`` object, created from the configuration file
      - ``error`` -- the function to call in case of configuration errors

    Return:
      - is the configuration valid ?
    """
    errors = list(_validate(filename, config))
    if errors:
        error('\n'.join(errors))
        return False

    return True
