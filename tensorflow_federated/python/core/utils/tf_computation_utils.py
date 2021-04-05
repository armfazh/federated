# Copyright 2018, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Defines utility functions/classes for constructing TF computations."""

import tensorflow as tf

from tensorflow_federated.python.common_libs import py_typecheck
from tensorflow_federated.python.common_libs import structure
from tensorflow_federated.python.core.api import computation_types


def create_variables(name, type_spec, **kwargs):
  """Creates a set of variables that matches the given `type_spec`.

  Unlike `tf.get_variables`, this method will always create new variables,
  and will not retrieve variables previously created with the same name.

  Args:
    name: The common name to use for the scope in which all of the variables are
      to be created.
    type_spec: An instance of `tff.Type` or something convertible to it. The
      type signature may only be composed of tensor types and named tuples,
      possibly nested.
    **kwargs: Additional keyword args to pass to `tf.Variable` construction.

  Returns:
    Either a single variable when invoked with a tensor TFF type, or a nested
    structure of variables created in the appropriately-named variable scopes
    made up of anonymous tuples if invoked with a named tuple TFF type.

  Raises:
    TypeError: if `type_spec` is not a type signature composed of tensor and
      named tuple TFF types.
  """
  py_typecheck.check_type(name, str)
  type_spec = computation_types.to_type(type_spec)
  if type_spec.is_tensor():
    return tf.Variable(
        initial_value=tf.zeros(dtype=type_spec.dtype, shape=type_spec.shape),
        name=name,
        **kwargs)
  elif type_spec.is_struct():

    def _scoped_name(var_name, index):
      if var_name is None:
        var_name = str(index)
      if name:
        return '{}/{}'.format(name, var_name)
      else:
        return var_name

    type_elements_iter = structure.iter_elements(type_spec)
    return structure.Struct(
        (k, create_variables(_scoped_name(k, i), v, **kwargs))
        for i, (k, v) in enumerate(type_elements_iter))
  else:
    raise TypeError(
        'Expected a TFF type signature composed of tensors and named tuples, '
        'found {}.'.format(type_spec))

