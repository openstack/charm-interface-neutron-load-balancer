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

# the reactive framework unfortunately does not grok `import as` in conjunction
# with decorators on class instance methods, so we have to revert to `from ...`
# imports
from charms.reactive import (
    Endpoint,
    clear_flag,
    set_flag,
    when_all,
    when_not,
)


class NeutronLoadBalancerRequires(Endpoint):
    @when_all('endpoint.{endpoint_name}.joined',
              'endpoint.{endpoint_name}.changed.neutron-api-ready')
    def joined(self):
        clear_flag(
            self.expand_name(
                'endpoint.{endpoint_name}.changed.neutron-api-ready'))
        set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

    def publish_load_balancer_info(self, name, base_url):
        for relation in self.relations:
            relation.to_publish['name'] = name
            relation.to_publish['base_url'] = base_url
