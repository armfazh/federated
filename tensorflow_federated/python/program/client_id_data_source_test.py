# Copyright 2022, The TensorFlow Federated Authors.
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

from absl.testing import absltest
from absl.testing import parameterized

from tensorflow_federated.python.program import client_id_data_source


class ClientIdDataSourceIteratorTest(parameterized.TestCase):

  def test_init_does_not_raise_type_error(self):
    client_ids = ['a', 'b', 'c']

    try:
      client_id_data_source.ClientIdDataSourceIterator(client_ids=client_ids)
    except TypeError:
      self.fail('Raised `TypeError` unexpectedly.')

  @parameterized.named_parameters(
      ('none', None),
      ('bool', True),
      ('int', 1),
      ('list', [True, 1, 'a']),
  )
  def test_init_raises_type_error_with_client_ids(self, client_ids):
    with self.assertRaises(TypeError):
      client_id_data_source.ClientIdDataSourceIterator(client_ids=client_ids)

  def test_init_raises_value_error_with_client_ids_empty(self):
    client_ids = []
    with self.assertRaises(ValueError):
      client_id_data_source.ClientIdDataSourceIterator(client_ids=client_ids)

  @parameterized.named_parameters(
      ('1', 0),
      ('2', 1),
      ('3', 2),
  )
  def test_select_returns_data(self, number_of_clients):
    client_ids = ['a', 'b', 'c']
    iterator = client_id_data_source.ClientIdDataSourceIterator(
        client_ids=client_ids)

    actual_client_ids = iterator.select(number_of_clients)

    self.assertLen(actual_client_ids, number_of_clients)
    for actual_client_id in actual_client_ids:
      self.assertIn(actual_client_id, client_ids)
      self.assertIsInstance(actual_client_id, str)

  @parameterized.named_parameters(
      ('str', 'a'),
      ('list', []),
  )
  def test_select_raises_type_error_with_number_of_clients(
      self, number_of_clients):
    client_ids = ['a', 'b', 'c']
    iterator = client_id_data_source.ClientIdDataSourceIterator(
        client_ids=client_ids)

    with self.assertRaises(TypeError):
      iterator.select(number_of_clients)

  @parameterized.named_parameters(
      ('none', None),
      ('negative', -1),
      ('greater', 4),
  )
  def test_select_raises_value_error_with_number_of_clients(
      self, number_of_clients):
    client_ids = ['a', 'b', 'c']
    iterator = client_id_data_source.ClientIdDataSourceIterator(
        client_ids=client_ids)

    with self.assertRaises(ValueError):
      iterator.select(number_of_clients)


class ClientIdDataSourceTest(parameterized.TestCase):

  @parameterized.named_parameters(
      ('none', None),
      ('bool', True),
      ('int', 1),
      ('list', [True, 1, 'a']),
  )
  def test_init_raises_type_error_with_client_ids(self, client_ids):
    with self.assertRaises(TypeError):
      client_id_data_source.ClientIdDataSource(client_ids)

  def test_init_raises_value_error_with_client_ids_empty(self):
    client_ids = []
    with self.assertRaises(ValueError):
      client_id_data_source.ClientIdDataSource(client_ids)


if __name__ == '__main__':
  absltest.main()
