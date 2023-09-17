# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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
"""Flags and helpers for the compute service-attachment commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.command_lib.compute import completers as compute_completers
from googlecloudsdk.command_lib.compute import flags as compute_flags

DEFAULT_LIST_FORMAT = """\
    table(
      name,
      region.basename(),
      targetService.basename(),
      connection_preference
    )"""


class ServiceAttachmentsCompleter(compute_completers.ListCommandCompleter):

  def __init__(self, **kwargs):
    super(ServiceAttachmentsCompleter, self).__init__(
        collection='compute.serviceAttachments',
        list_command='compute service-attachments list --uri',
        **kwargs)


def AddDescription(parser):
  parser.add_argument(
      '--description',
      help='An optional, textual description for the service attachment.')


def AddConnectionPreference(parser, is_update=False):
  connection_preference_choices = {
      'ACCEPT_AUTOMATIC':
          'Always accept connection requests from consumers automatically.',
      'ACCEPT_MANUAL':
          'Only accept connection requests from consumers with the approval of '
          'the service provider.',
  }

  parser.add_argument(
      '--connection-preference',
      choices=connection_preference_choices,
      type=lambda x: x.replace('-', '_').upper(),
      default=None if is_update else 'ACCEPT_AUTOMATIC',
      help="This defines the service attachment's connection preference.")


def AddEnableProxyProtocolForCreate(parser):
  parser.add_argument(
      '--enable-proxy-protocol',
      action='store_true',
      default=False,
      help="""\
      If True, then enable the proxy protocol which is for supplying client
      TCP/IP address data in TCP connections that traverse proxies on their way
      to destination servers.
      """)


def AddEnableProxyProtocolForUpdate(parser):
  parser.add_argument(
      '--enable-proxy-protocol',
      action=arg_parsers.StoreTrueFalseAction,
      help="""\
      If True, then enable the proxy protocol which is for supplying client
      TCP/IP address data in TCP connections that traverse proxies on their way
      to destination servers.
      """)


def AddDomainNames(parser):
  parser.add_argument(
      '--domain-names',
      type=arg_parsers.ArgList(),
      metavar='DOMAIN_NAMES',
      default=None,
      help="""\
      Specifies a comma separated list of DNS domain names that are used during
      DNS integration on PSC connected endpoints.
      """)


def AddConsumerRejectList(parser):
  parser.add_argument(
      '--consumer-reject-list',
      type=arg_parsers.ArgList(),
      metavar='REJECT_LIST',
      default=None,
      help="""\
      Specifies a comma separated list of projects that are not allowed to
      connect to this service attachment. The project can be specified using its
      id or number.
      """)


def AddConsumerRejectListAlpha(parser):
  parser.add_argument(
      '--consumer-reject-list',
      type=arg_parsers.ArgList(),
      metavar='REJECT_LIST',
      default=None,
      help="""\
      Specifies a comma separated list of projects or networks that are not
      allowed to connect to this service attachment. The project can be
      specified using its project ID or project number and the network can be
      specified using its URL. A given service attachment can manage connections
      at either the project or network level. Therefore, both the reject and
      accept lists for a given service attachment must contain either only
      projects or only networks.""")


def AddConsumerAcceptList(parser):
  parser.add_argument(
      '--consumer-accept-list',
      type=arg_parsers.ArgDict(),
      action='append',
      metavar='PROJECT=LIMIT',
      default=None,
      help="""\
      Adds consumer project(s) with connection limit(s) to the accept list of
      the service attachment.

      For example, `--consumer-accept-list myProjectId1=20` accepts a consumer
      project myProjectId1 with connection limit 20.

      * `PROJECT_ID_OR_NUM` - Consumer project id or number.
      * `CONNECTION_LIMIT` - The max number of allowed connections.
      """)


def AddConsumerAcceptListAlpha(parser):
  parser.add_argument(
      '--consumer-accept-list',
      type=arg_parsers.ArgDict(),
      action='append',
      metavar='PROJECT_OR_NETWORK=LIMIT',
      default=None,
      help="""\
    Specifies which consumer projects or networks are allowed to connect to the
    service attachment. Each project or network has a connection limit. A given
    service attachment can manage connections at either the project or network
    level. Therefore, both the accept and reject lists for a given service
    attachment must contain either only projects or only networks.

    For example, `--consumer-accept-list myProjectId1=20` accepts a consumer
    project myProjectId1 with connection limit 20;
    `--consumer-accept-list projects/myProjectId1/global/networks/myNet1=20`
    accepts a consumer network myNet1 with connection limit 20

    * `PROJECT_OR_NETWORK` - Consumer project ID, project number or network URL.
    * `CONNECTION_LIMIT` - The maximum number of allowed connections.
    """)


def ServiceAttachmentArgument(required=True, plural=False):
  return compute_flags.ResourceArgument(
      resource_name='service attachment',
      completer=ServiceAttachmentsCompleter,
      plural=plural,
      required=required,
      regional_collection='compute.serviceAttachments',
      region_explanation=compute_flags.REGION_PROPERTY_EXPLANATION)
