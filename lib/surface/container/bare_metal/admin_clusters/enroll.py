# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command to enroll an admin cluster in an Anthos cluster on bare metal."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.gkeonprem import bare_metal_admin_clusters as apis
from googlecloudsdk.api_lib.container.gkeonprem import operations
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.bare_metal import admin_cluster_flags as cluster_flags
from googlecloudsdk.command_lib.container.gkeonprem import flags

_EXAMPLES = """
To enroll a cluster named ``my-cluster'' managed in location ``us-west1''
with admin cluster membership of
``projects/my-project/locations/us-west1/memberships/my-admin-cluster-membership'',
run:

$ {command} my-cluster --location=us-west1 --admin-cluster-membership=projects/my-project/locations/us-west1/memberships/my-admin-cluster-membership
"""


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Enroll(base.Command):
  """Enroll an Anthos on bare metal admin cluster."""

  @staticmethod
  def Args(parser):
    flags.AddAdminClusterMembershipResourceArg(parser, positional=False)
    cluster_flags.AddAdminClusterResourceArg(parser, 'to enroll')
    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    cluster_client = apis.AdminClustersClient()
    operation = cluster_client.Enroll(args)

    if args.async_:
      return operation
    else:
      operation_client = operations.OperationsClient()
      return operation_client.Wait(operation)
