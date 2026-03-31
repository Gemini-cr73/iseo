import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.core.db import get_conn


def new_trace_id() -> str:
    return uuid.uuid4().hex


def audit_event(
    *,
    trace_id: str,
    actor: str,
    event_type: str,
    input_obj: dict[str, Any] | None = None,
    output_obj: dict[str, Any] | None = None,
    notes: str | None = None,
) -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO audit_events (ts, trace_id, actor, event_type, input_json, output_json, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(UTC).isoformat(),
            trace_id,
            actor,
            event_type,
            json.dumps(input_obj) if input_obj is not None else None,
            json.dumps(output_obj) if output_obj is not None else None,
            notes,
        ),
    )

    conn.commit()
    conn.close()
