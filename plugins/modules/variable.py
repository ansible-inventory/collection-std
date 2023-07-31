#!/usr/bin/env python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: variable

short_description: Manipulate Isidore variables

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.0"

description: Set, unset, and append to Isidore variables

options:
    name:
        description: The name of the variable to manipulate
        required: true
        type: str
    state:
        description:
	    - The state of the variable. Can be `present` to set the variable
	    - to the specified value, `absent` to unset the variable, or
	    - `append` to append the value to a list variable.
	default: present
        required: false
        type: list
	elements:
	    - present
	    - absent
	    - append
    value:
        description:
	    - The value to set for (or append to) the variable. Required when
	      state is present or append.
	    required: false
        type: freeform
	
extends_documentation_fragment:
    - isidore.std.variable

author:
    - Scott Court (@Z5T1)
'''

EXAMPLES = r'''
# Set the variable foo to value 42
- name: Set the foo variable
  isidore.std.variable:
    name: foo
    value: 42

# Unset the variable bar
- name: Unset the variable bar
  isidore.std.variable:
    name: bar
    state: absent

# Append the value 4 to the end of the list variable qux
- name: Append the value 4 to the list variable qux
  isidore.std.variable:
    name: qux
    state: append
    value: 4
'''

RETURN = r'''
# None
'''

from ansible.module_utils.basic import AnsibleModule
from isidore.libIsidore import *


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
	state=dict(type='list', required=False, default='present'),
        value=dict(type='freeform', required=False, default=None)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    #result['original_message'] = module.params['name']
    #result['message'] = 'goodbye'

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()


