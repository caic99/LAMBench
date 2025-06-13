import pytest
import sys
from types import ModuleType
from unittest.mock import MagicMock

# Mock dflow modules so that lambench.workflow.dflow can be imported without
# installing the real dflow dependencies.
dflow = ModuleType("dflow")
dflow.Task = MagicMock()
dflow.Workflow = MagicMock()
sys.modules.setdefault("dflow", dflow)

dflow_python = ModuleType("dflow.python")


class DummyOP:
    @staticmethod
    def function(func):
        return func


dflow_python.OP = DummyOP
dflow_python.Artifact = MagicMock
dflow_python.PythonOPTemplate = MagicMock
sys.modules.setdefault("dflow.python", dflow_python)

sys.modules.setdefault("dflow.plugins", ModuleType("dflow.plugins"))

bohrium = ModuleType("dflow.plugins.bohrium")
bohrium.BohriumDatasetsArtifact = MagicMock
bohrium.create_job_group = MagicMock(return_value=1)
sys.modules.setdefault("dflow.plugins.bohrium", bohrium)

dispatcher = ModuleType("dflow.plugins.dispatcher")
dispatcher.DispatcherExecutor = MagicMock
sys.modules.setdefault("dflow.plugins.dispatcher", dispatcher)

from lambench.models.dp_models import DPModel  # noqa: E402
from lambench.tasks import DirectPredictTask  # noqa: E402
from lambench.workflow.dflow import submit_tasks_dflow  # noqa: E402


def test_submit_tasks_dflow_requires_skip(valid_model_data, direct_task_data):
    model = DPModel(**valid_model_data)
    task = DirectPredictTask(**direct_task_data)
    with pytest.raises(ValueError):
        submit_tasks_dflow([(task, model)], skip_database=False)
