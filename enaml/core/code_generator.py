#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from contextlib import contextmanager

from atom.api import Atom, List, Str

from . import byteplay as bp


class CodeGenerator(Atom):
    """ A class for generating bytecode operations.

    """
    #: The full name of the file which is being compiled.
    filename = Str()

    #: The list of generated byteplay code operations.
    code_ops = List()

    def set_lineno(self, lineno):
        """ Set the current line number in the code.

        """
        self.code_ops.append(                           # TOS
            (bp.SetLineno, lineno),                     # TOS
        )

    def load_global(self, name):
        """ Load a global variable onto the TOS.

        """
        self.code_ops.append(                           # TOS
            (bp.LOAD_GLOBAL, name),                     # TOS -> value
        )

    def load_fast(self, name):
        """ Load a fast local variable onto the TOS.

        """
        self.code_ops.append(                           # TOS
            (bp.LOAD_FAST, name),                       # TOS -> value
        )

    def load_name(self, name):
        """ Load a named value onto the TOS.

        """
        self.code_ops.append(                           # TOS
            (bp.LOAD_NAME, name),                       # TOS -> value
        )

    def load_const(self, const):
        """ Load a const value onto the TOS.

        """
        self.code_ops.append(                           # TOS
            (bp.LOAD_CONST, const),                     # TOS -> value
        )

    def load_attr(self, name):
        """ Load an attribute from the object on TOS.

        """
        self.code_ops.append(                           # TOS -> obj
            (bp.LOAD_ATTR, name),                       # TOS -> value
        )

    def store_global(self, name):
        """ Store the TOS as a global.

        """
        self.code_ops.append(                           # TOS -> value
            (bp.STORE_GLOBAL, name),                    # TOS
        )

    def store_fast(self, name):
        """ Store the TOS as a fast local.

        """
        self.code_ops.append(                           # TOS -> value
            (bp.STORE_FAST, name),                      # TOS
        )

    def store_attr(self, name):
        """ Store the value at 2nd as an attr on 1st.

        """
        self.code_ops.append(                           # TOS -> val -> obj
            (bp.STORE_ATTR, name),                      # TOS
        )

    def delete_global(self, name):
        """ Delete a named global variable.

        """
        self.code_ops.append(                           # TOS
            (bp.DELETE_GLOBAL, name),                   # TOS
        )

    def delete_fast(self, name):
        """ Delete a named fast local variable.

        """
        self.code_ops.append(                           # TOS
            (bp.DELETE_FAST, name),                     # TOS
        )

    def return_value(self):
        """ Return the value from the TOS.

        """
        self.code_ops.append(                           # TOS -> value
            (bp.RETURN_VALUE, None),                    # TOS
        )

    def dup_top(self):
        """ Duplicate the value on the TOS.

        """
        self.code_ops.append(                           # TOS -> value
            (bp.DUP_TOP, None),                         # TOS -> value -> value
        )

    def build_map(self, n=0):
        """ Build a map and store it onto the TOS.

        """
        self.code_ops.append(                           # TOS
            (bp.BUILD_MAP, n),                          # TOS -> map
        )

    def build_tuple(self, n=0):
        """ Build a tuple from items on the TOS.

        """
        if n == 0:
            self.code_ops.append(                       # TOS
                (bp.LOAD_CONST, ()),                    # TOS -> tuple
            )
        else:
            self.code_ops.append(                       # TOS
                (bp.BUILD_TUPLE, n),                    # TOS -> tuple
            )

    def store_map(self):
        """ Store the key/value pair on the TOS into the map a 3rd pos.

        """
        self.code_ops.append(                           # TOS -> map -> value -> key
            (bp.STORE_MAP, None),                       # TOS -> map
        )

    def build_class(self):
        """ Build a class from the top 3 stack items.

        """
        self.code_ops.append(                           # TOS -> name -> bases -> dict
            (bp.BUILD_CLASS, None),                     # TOS -> class
        )

    def make_function(self, n_defaults=0):
        """ Make a function from a code object on the TOS.

        """
        self.code_ops.append(                           # TOS -> code -> defaults
            (bp.MAKE_FUNCTION, n_defaults),             # TOS -> func
        )

    def call_function(self, n_args=0, n_kwds=0):
        """ Call a function on the TOS with the given args and kwargs.

        """
        argspec = ((n_kwds & 0xFF) << 8) + (n_args & 0xFF)
        self.code_ops.append(                           # TOS -> func -> args -> kwargs
            (bp.CALL_FUNCTION, argspec),                # TOS -> retval
        )

    def call_function_var(self, n_args=0, n_kwds=0):
        """ Call a var function on the TOS with the given args and kwargs.

        """
        argspec = ((n_kwds & 0xFF) << 8) + (n_args & 0xFF)
        self.code_ops.append(                           # TOS -> func -> args -> kwargs -> varargs
            (bp.CALL_FUNCTION_VAR, argspec),            # TOS -> retval
        )

    def pop_top(self):
        """ Pop the value from the TOS.

        """
        self.code_ops.append(                           # TOS -> value
            (bp.POP_TOP, None),                         # TOS
        )

    def rot_two(self):
        """ Rotate the two values on the TOS.

        """
        self.code_ops.append(                           # TOS -> val_1 -> val_2
            (bp.ROT_TWO, None),                         # TOS -> val_2 -> val_1
        )

    def rot_three(self):
        """ Rotate the three values on the TOS.

        """
        self.code_ops.append(                           # TOS -> val_1 -> val_2 -> val_3
            (bp.ROT_THREE, None),                       # TOS -> val_3 -> val_1 -> val_2
        )

    def reverse_three(self):
        """ Reverse the three values on the TOS.

        """
        self.rot_three()
        self.rot_two()

    def load_globals(self):
        """ Load the globals onto the TOS.

        """
        self.code_ops.extend([                          # TOS
            (bp.LOAD_GLOBAL, 'globals'),                # TOS -> func
            (bp.CALL_FUNCTION, 0x0000),                 # TOS -> globals
        ])

    def store_globals_to_fast(self):
        """ Store the globals to the fast locals.

        """
        self.code_ops.extend([                          # TOS
            (bp.LOAD_GLOBAL, 'globals'),                # TOS -> func
            (bp.CALL_FUNCTION, 0x0000),                 # TOS -> globals
            (bp.STORE_FAST, '_[f_globals]'),            # TOS
        ])

    def load_globals_from_fast(self):
        """ Load the stored globals from the fast locals.

        """
        self.code_ops.append(                           # TOS
            (bp.LOAD_FAST, '_[f_globals]'),             # TOS -> globals
        )

    def load_helper(self, name):
        """ Load a named compiler helper onto the TOS.

        """
        self.code_ops.extend([                          # TOS
            (bp.LOAD_GLOBAL, '__compiler_helpers'),     # TOS -> helpers
            (bp.LOAD_CONST, name),                      # TOS -> helpers -> name
            (bp.BINARY_SUBSCR, None),                   # TOS -> helper
        ])

    def store_helpers_to_fast(self):
        """ Store the compiler helpers to the fast locals.

        """
        self.code_ops.extend([                          # TOS
            (bp.LOAD_GLOBAL, '__compiler_helpers'),     # TOS -> helpers
            (bp.STORE_FAST, '_[helpers]'),              # TOS
        ])

    def load_helper_from_fast(self, name):
        """ Load the stored helper from the fast locals.

        """
        self.code_ops.extend([                          # TOS
            (bp.LOAD_FAST, '_[helpers]'),               # TOS -> helpers
            (bp.LOAD_CONST, name),                      # TOS -> helpers -> name
            (bp.BINARY_SUBSCR, None),                   # TOS -> helper
        ])

    @contextmanager
    def try_squash_raise(self):
        """ A context manager for squashing tracebacks.

        The code written during this context will be wrapped so that
        any exception raised will appear to have been generated from
        the code, rather than any function called by the code.

        """
        exc_label = bp.Label()
        end_label = bp.Label()
        self.code_ops.append(
            (bp.SETUP_EXCEPT, exc_label),               # TOS
        )
        yield
        self.code_ops.extend([                          # TOS
            (bp.POP_BLOCK, None),                       # TOS
            (bp.JUMP_FORWARD, end_label),               # TOS
            (exc_label, None),                          # TOS -> tb -> val -> exc
            (bp.ROT_THREE, None),                       # TOS -> exc -> tb -> val
            (bp.ROT_TWO, None),                         # TOS -> exc -> val -> tb
            (bp.POP_TOP, None),                         # TOS -> exc -> val
            (bp.RAISE_VARARGS, 2),                      # TOS
            (bp.JUMP_FORWARD, end_label),               # TOS
            (bp.END_FINALLY, None),                     # TOS
            (end_label, None),                          # TOS
        ])

    @contextmanager
    def for_loop(self, iter_var, fast_var=True):
        """ A context manager for creating for-loops.

        Parameters
        ----------
        iter_var : str
            The name of the loop iter variable.

        fast_var : bool, optional
            Whether the iter_var lives in fast locals. The default is
            True. If False, the iter_var is loaded from globals.

        """
        start_label = bp.Label()
        jump_label = bp.Label()
        end_label = bp.Label()
        load_op = bp.LOAD_FAST if fast_var else bp.LOAD_GLOBAL
        self.code_ops.extend([
            (bp.SETUP_LOOP, end_label),
            (load_op, iter_var),
            (bp.GET_ITER, None),
            (start_label, None),
            (bp.FOR_ITER, jump_label),
        ])
        yield
        self.code_ops.extend([
            (bp.JUMP_ABSOLUTE, start_label),
            (jump_label, None),
            (bp.POP_BLOCK, None),
            (end_label, None),
        ])

    def insert_python_block(self, pydata, trim=True):
        """ Insert the compiled code for a Python Module ast or string.

        """
        code = compile(pydata, self.filename, mode='exec')
        bp_code = bp.Code.from_code(code).code
        if trim:  # skip SetLineno and ReturnValue
            bp_code = bp_code[1:-2]
        self.code_ops.extend(bp_code)

    def insert_python_expr(self, pydata, trim=True):
        """ Insert the compiled code for a Python Expression ast or string.

        """
        code = compile(pydata, self.filename, mode='eval')
        bp_code = bp.Code.from_code(code).code
        if trim:  # skip ReturnValue
            bp_code = bp_code[:-1]
        self.code_ops.extend(bp_code)

    def rewrite_to_fast_locals(self, local_names):
        """ Rewrite the locals to be loaded from fast locals.

        Given a set of available local names, this method will rewrite
        the current code ops, replaces every instance of a *_NAME opcode
        with a *_FAST or *_GLOBAL depending on whether or not the name
        exists in local_names or was written via STORE_NAME. This method
        is useful to convert the code so it can be used as a function.

        Parameters
        ----------
        local_names : set
            The set of available locals for the code.

        Returns
        -------
        result : list
            The list of names which must be provided as arguments.

        """
        arg_names = []
        stored_names = set()
        code_ops = self.code_ops
        for idx, (op, op_arg) in enumerate(code_ops):
            if op == bp.STORE_NAME:
                stored_names.add(op_arg)
                code_ops[idx] = (bp.STORE_FAST, op_arg)
        for idx, (op, op_arg) in enumerate(code_ops):
            if op == bp.LOAD_NAME:
                if op_arg in local_names:
                    op = bp.LOAD_FAST
                    arg_names.append(op_arg)
                elif op_arg in stored_names:
                    op = bp.LOAD_FAST
                else:
                    op = bp.LOAD_GLOBAL
                code_ops[idx] = (op, op_arg)
            elif op == bp.DELETE_NAME:          # py2.6 list comps
                if op_arg in stored_names:
                    op = bp.DELETE_FAST
                else:
                    op = bp.DELETE_GLOBAL
                code_ops[idx] = (op, op_arg)
        return arg_names

    def to_code(self, freevars=[], args=[], varargs=False, varkwargs=False,
                newlocals=False, name='', firstlineno=0, docstring=None):
        """ Create a Python code object from the current code ops.

        """
        bp_code = bp.Code(
            self.code_ops, freevars[:], args[:], varargs, varkwargs,
            newlocals, name, self.filename, firstlineno, docstring,
        )
        return bp_code.to_code()