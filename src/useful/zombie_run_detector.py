from datetime import timedelta

from prefect.automations import Automation
from prefect.client.schemas.objects import StateType
from prefect.events.actions import ChangeFlowRunState
from prefect.events.schemas.automations import EventTrigger, Posture
from prefect.events.schemas.events import ResourceSpecification


my_automation = Automation(
    name="Crash zombie flows",
    trigger=EventTrigger(
        after={"prefect.flow-run.heartbeat"},
        expect={
            "prefect.flow-run.heartbeat",
            "prefect.flow-run.Completed",
            "prefect.flow-run.Failed",
            "prefect.flow-run.Cancelled",
            "prefect.flow-run.Crashed",
        },
        match=ResourceSpecification({"prefect.resource.id": ["prefect.flow-run.*"]}),
        for_each={"prefect.resource.id"},
        posture=Posture.Proactive,
        threshold=1,
        within=timedelta(seconds=90),
    ),
    actions=[
        ChangeFlowRunState(
            state=StateType.CRASHED,
            message="Flow run marked as crashed due to missing heartbeats.",
        ) # type: ignore
    ],
)

if __name__ == "__main__":
    my_automation.create()

