#!/usr/bin/env python3

# Copyright © 2023 Scott Court
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the “Software”), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from isidore.libIsidore import *

display = Display()

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        # Get module arguments
        hostname = self._templar.template("{{ inventory_hostname }}")
        name = module_args.get('name')
        value = module_args.get('value')
        state = module_args.get('state')
        if state == None:
            state = 'present'

        # Debug: print parsed module argument values
        display.vvv('''%s:
        name: %s
        value: %s
        state: %s''' % (hostname, name, value, state) )

        # Set necessary Isidore variables
        isidore = Isidore.fromConfigFile()
        host = isidore.getHost(hostname)
        old_value = host.getVar(name)

        # Debug: print Isidore variables
        display.vvv('''        Isidore hostname: %s
        old value: %s''' % (host.getHostname(), old_value))

        if state == 'present':
            if self._play_context.check_mode == False:
                host.setVar(name, value)
            result['changed'] = False if old_value == value else True

        elif state == 'absent':
            if self._play_context.check_mode == False:
                host.unsetVar(name)
            result['changed'] = False if old_value == None else True

        elif state == 'append':
            if type(old_value) != list:
                result['failed'] = True
                result['message'] = 'Variable %s is not a list' % (name)
                return result

            if self._play_context.check_mode == False:
                host.appendVar(name, value)
            result['changed'] = True

        return result

