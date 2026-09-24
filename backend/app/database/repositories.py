from uuid import UUID

from sqlmodel import col, select

from app.database.abstract_repository import AbstractRepository
from app.database.engine import get_db_session
from app.database.models import Command, CommandHistory, MainCommand


class MainCommandRepository(AbstractRepository[MainCommand, int]):
    """
    Repository for MainCommand table.
    """

    model = MainCommand


class CommandsRepository(AbstractRepository[Command, UUID]):
    """
    Repository for Command table.
    """

    model = Command


class CommandHistoryRepository(AbstractRepository[CommandHistory, UUID]):
    """
    Repository for Command table.
    """

    model = CommandHistory

    async def get_history_by_id(self, command_id: UUID) -> list[CommandHistory]:
        """
        Get the entire history of a command by its UUID, sorted by latest first.
        """
        # commands: list[CommandHistory] = await self.get_all_by(command_id=command_id)

        async with get_db_session() as session:
            cur_command_history = list(
                (
                    await session.exec(
                        select(self.model)
                        .where(self.model.command_id == command_id)
                        .order_by(col(self.model.created_at).desc())
                    )
                ).all()
            )

        # cur_command_history = sorted(cur_command_history, key=lambda x: x.created_at, reverse=True)
        # command_history = self.get_by_id(command_id)
        # print(cur_command_history)
        return cur_command_history
