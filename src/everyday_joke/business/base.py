from typing import Any, Protocol


class Interactor(Protocol):
    async def __call__(self, data: Any) -> Any:
        ...
