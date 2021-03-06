# Copyright 2017 Google Inc. All Rights Reserved.
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
"""Sets the IAM policy for the repository."""

from googlecloudsdk.api_lib.sourcerepo import sourcerepo
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.iam import iam_util
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.GA, base.ReleaseTrack.ALPHA,
                    base.ReleaseTrack.BETA)
class SetIamPolicy(base.UpdateCommand):
  """Set the IAM policy for the named repository.

  This command sets the IAM policy for the given repository from the
  policy in the provided file.

  ## EXAMPLES

  To set the IAM policy, issue the following command:

    $ {command} REPOSITORY_NAME POLICY_FILE

  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'name', metavar='REPOSITORY_NAME', help='Name of the repository.')
    parser.add_argument(
        'policy_file',
        help=('JSON or YAML file with IAM policy. '
              'See https://cloud.google.com/resource-manager/'
              'reference/rest/Shared.Types/Policy'))
    parser.display_info.AddFormat('default')

  def Run(self, args):
    """Sets the IAM policy for the repository.

    Args:
      args: argparse.Namespace, the arguments this command is run with.

    Returns:
      (sourcerepo_v1_messsages.Policy) The IAM policy.

    Raises:
      ToolException: on project initialization errors.
    """
    res = resources.REGISTRY.Parse(
        args.name,
        params={'projectsId': properties.VALUES.core.project.GetOrFail},
        collection='sourcerepo.projects.repos')
    policy = iam_util.ParseYamlorJsonPolicyFile(args.policy_file,
                                                sourcerepo.messages.Policy)
    source = sourcerepo.Source()
    result = source.SetIamPolicy(res, policy)
    iam_util.LogSetIamPolicy(res.Name(), 'repo')
    return result
