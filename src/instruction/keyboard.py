# Copyright (c) 2016, BRML
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


class KeyboardInput(object):
    def __init__(self):
        """Request keyboard input from the user to instruct the demonstration
        task.
        Prints the instructions for the user to the console.
        """
        self._object_ids = {
            1: 'hand',
            2: 'remote',
            3: 'cellphone',
            4: 'mouse',
            5: 'bottle',
            6: 'cup',
            7: 'ball'
        }
        self._target_ids = {
            1: 'hand',
            2: 'table'
        }
        s = '\nDemonstration instruction:\n'
        s += 'Take object A (from my hand) and put it on the table (in my hand).\n'
        s += 'Select one object identifier out of\n'
        for k, v in sorted(self._object_ids.items()):
            s += '\t{}\t{}\n'.format(k, v)
        s += 'Select one target identifier out of\n'
        for k, v in sorted(self._target_ids.items()):
            s += '\t{}\t{}\n'.format(k, v)
        s += "To exit the demonstration, input '0'."
        print s

    def instruct(self):
        """Request two appropriate integer values keyboard input from the user.
        Return the corresponding object identifier and target identifier as a
        string, separating the two by a space. If exit is requested, return
        'exit' instead.
        """
        def get_int_in_dict(s, d):
            """Get an integer from keyboard input that is a key in a given dict.

            :param s: Instruction text for input() command.
            :param d: The dictionary.
            :return: The value in the dict corresponding to the input or
                'exit'.
            """
            valid = False
            while not valid:
                identifier = input(s)
                if not isinstance(identifier, int):
                    print "Identifier must be an integer. Try again."
                    continue
                if identifier == 0:
                    return 'exit'
                try:
                    return d[identifier]
                except KeyError:
                    print "Not a valid identifier. Try again."
                    continue

        oid = get_int_in_dict("Input integer object id: ", self._object_ids)
        if oid == 'exit':
            return oid
        tid = get_int_in_dict("Input integer target id: ", self._target_ids)
        if tid == 'exit':
            return tid
        return '{} {}'.format(oid, tid)
