# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requires

import charms_openstack.test_utils as test_utils


_hook_args = {}


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = []
        hook_set = {
            'when_all': {
                'joined': (
                    'endpoint.{endpoint_name}.joined',
                    'endpoint.{endpoint_name}.changed.neutron-api-ready',),
            },
            'when_not': {
                'broken': ('endpoint.{endpoint_name}.joined',),
            },
        }
        # test that the hooks were registered via the
        # reactive.barbican_handlers
        self.registered_hooks_test_helper(requires, hook_set, defaults)


class TestNeutronLoadBalancerRequires(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self.neutron_api_req = requires.NeutronLoadBalancerRequires(
            'some-relation', [])
        self._patches = {}
        self._patches_start = {}

    def tearDown(self):
        self.neutron_api_req = None
        for k, v in self._patches.items():
            v.stop()
            setattr(self, k, None)
        self._patches = None
        self._patches_start = None

    def test_joined(self):
        self.patch_object(requires, 'clear_flag')
        self.patch_object(requires, 'set_flag')
        self.neutron_api_req.joined()
        self.clear_flag.assert_called_once_with(
            'endpoint.some-relation.changed.neutron-api-ready')
        self.set_flag.assert_called_once_with('some-relation.available')

    def test_broken(self):
        self.patch_object(requires, 'clear_flag')
        self.neutron_api_req.broken()
        self.clear_flag.assert_called_once_with('some-relation.available')
