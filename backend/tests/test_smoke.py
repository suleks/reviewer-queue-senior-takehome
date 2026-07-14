import asyncio

import pytest
from fastapi import HTTPException

from app.main import ActionRequest, apply_action, health, list_review_items, reset_items


def run_async(coro):
    return asyncio.run(coro)


def test_health_check() -> None:
    assert run_async(health()) == {"status": "ok"}


def test_review_items_endpoint_returns_seed_data() -> None:
    response = run_async(list_review_items())
    assert len(response["items"]) > 0

@pytest.mark.parametrize("action", ["approve", "reject", "escalate"])
def test_unassigned_items_cannot_be_resolved(action: str) -> None:
    with pytest.raises(HTTPException) as exception:
        run_async(apply_action("RV-1024", ActionRequest(action=action)))

    assert exception.value.status_code == 409
    assert exception.value.detail == "Only assigned items can be actioned"


@pytest.mark.parametrize("item_id", ["RV-1029", "RV-1033", "RV-1034"])
@pytest.mark.parametrize("action", ["approve", "reject", "escalate"])
def test_resolved_items_cannot_be_resolved_again(item_id: str, action: str) -> None:
    with pytest.raises(HTTPException) as exception:
        run_async(apply_action(item_id, ActionRequest(action=action)))

    assert exception.value.status_code == 409
    assert exception.value.detail == "This item has already been resolved"


def test_assigned_reviewer_can_release_task() -> None:
    try:
        response = run_async(
            apply_action("RV-1030", ActionRequest(action="release", reviewer="alex"))
        )
    finally:
        run_async(reset_items())

    assert response["item"]["status"] == "unassigned"
    assert response["item"]["assigned_reviewer"] is None


def test_unassigned_reviewer_cannot_release_task() -> None:
    with pytest.raises(HTTPException) as exception:
        run_async(apply_action("RV-1030", ActionRequest(action="release", reviewer="sam")))

    assert exception.value.status_code == 409
    assert exception.value.detail == "Only the assigned reviewer can release this item"