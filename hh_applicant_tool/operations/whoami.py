# Этот модуль можно использовать как образец для других
from __future__ import annotations

import argparse
import logging
from typing import TYPE_CHECKING
import json

from ..main import BaseOperation
from ..main import Namespace as BaseNamespace

if TYPE_CHECKING:
    from ..main import HHApplicantTool


logger = logging.getLogger(__package__)


class Namespace(BaseNamespace):
    pass


def fmt_plus(n: int) -> str:
    assert n >= 0
    return f"+{n}" if n else "0"


class Operation(BaseOperation):
    """Выведет текущего пользователя"""

    __aliases__: tuple[str] = ("id",)

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        pass

    def run(self, applicant_tool: HHApplicantTool) -> None:
        api_client = applicant_tool.api_client
        result = api_client.get("me")
        full_name = " ".join(
            filter(
                None,
                [
                    result.get("last_name"),
                    result.get("first_name"),
                    result.get("middle_name"),
                ],
            )
        )
        counters = result["counters"]

        # Формируем словарь
        data = {
            "id": result["id"],
            "name": full_name or "Анонимный аккаунт"
        }

        print(json.dumps(data, ensure_ascii=False))