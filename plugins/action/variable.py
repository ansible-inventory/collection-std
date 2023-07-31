#!/usr/bin/env python3
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

