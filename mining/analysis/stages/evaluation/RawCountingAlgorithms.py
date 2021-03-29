from analysis.stages.evaluation.CouplingAlgorithm import CouplingAlgorithm
from util.ArtifactStore import ArtifactStore
from util.CouplingCommit import CouplingCommit
from util.assertions import assert_modification_file_path
from .CouplingAlgorithm import CouplingAlgorithm


class UndirectedRawCountingAlgorithm(CouplingAlgorithm):

  def process_commit(self, cli_args, commit: CouplingCommit, commits, artifacts_store: ArtifactStore, graph_data):
    raw_counting(cli_args, commit, commits, artifacts_store, graph_data)

  def construct_graph(self, cli_args, graph_data, artifacts_store: ArtifactStore):
    graph = {'nodes': [], 'edges': []}

    if 'artifacts' in graph_data:
      for artifact_id, change_count in graph_data['artifacts'].items():
        graph['nodes'].append({
            'id': artifact_id,
            'label': artifacts_store.get_artifact_file_name(artifact_id),
            'value': change_count
        })

    if 'couplings' in graph_data:
      for coupling_id, change_count in graph_data['couplings'].items():
        artifacts = artifacts_from_coupling(coupling_id)
        graph['edges'].append({
            'id': coupling_id,
            'directed': False,
            'start': artifacts[0],
            'end': artifacts[1],
            'weight': change_count
        })

    return graph


class DirectedRawCountingAlgorithm(CouplingAlgorithm):

  def process_commit(self, cli_args, commit: CouplingCommit, commits, artifacts_store: ArtifactStore, graph_data):
    raw_counting(cli_args, commit, commits, artifacts_store, graph_data)

  def construct_graph(self, cli_args, graph_data, artifacts_store: ArtifactStore):
    graph = {'nodes': [], 'edges': []}

    if 'artifacts' in graph_data:
      for artifact_id, change_count in graph_data['artifacts'].items():
        graph['nodes'].append({
            'id': artifact_id,
            'label': artifacts_store.get_artifact_file_name(artifact_id),
            'value': change_count
        })

    if 'couplings' in graph_data:
      for coupling_id, change_count in graph_data['couplings'].items():
        artifacts = artifacts_from_coupling(coupling_id)
        graph['edges'].append({
            'id': coupling_id,
            'directed': True,
            'start': artifacts[0],
            'end': artifacts[1],
            'weight': change_count / graph_data['artifacts'][artifacts[0]]
        })
        graph['edges'].append({
            'id': inverted_coupling_id(coupling_id),
            'directed': True,
            'start': artifacts[1],
            'end': artifacts[0],
            'weight': change_count / graph_data['artifacts'][artifacts[1]]
        })

    return graph


def raw_counting(cli_args, commit: CouplingCommit, commits, artifacts_store: ArtifactStore, graph_data):
  if not 'artifacts' in graph_data:
    graph_data['artifacts'] = {}
  if not 'couplings' in graph_data:
    graph_data['couplings'] = {}

  def count_artifact_modification(artifact):
    if artifact.id in graph_data['artifacts']:
      graph_data['artifacts'][artifact.id] += 1
    else:
      graph_data['artifacts'][artifact.id] = 1

  def count_artifact_coupling(artifact1, artifact2):
    coupling_id = "::".join(sorted([artifact1.id, artifact2.id]))
    if coupling_id in graph_data['couplings']:
      graph_data['couplings'][coupling_id] += 1
    else:
      graph_data['couplings'][coupling_id] = 1

  if not commit.ignored:
    for modifications_bucket in commit.modifications_buckets:
      all_modifications = modifications_bucket.get_all_modifications(commits, commit)
      for (modification, commit_hash) in all_modifications:
        path = assert_modification_file_path(modification, commit_hash)
        artifact = artifacts_store.get_artifact(commit_hash, path)
        if artifact:
          count_artifact_modification(artifact)
          for (other_modification, other_commit_hash) in all_modifications:
            other_path = assert_modification_file_path(other_modification, other_commit_hash)
            other_artifact = artifacts_store.get_artifact(other_commit_hash, other_path)
            if other_artifact:
              if other_artifact.id != artifact.id:
                count_artifact_coupling(artifact, other_artifact)
              else:
                break


def artifacts_from_coupling(coupling: str):
  return coupling.split("::")


def inverted_coupling_id(coupling: str):
  artifacts = artifacts_from_coupling(coupling)
  return "::".join([artifacts[1], artifacts[0]])
