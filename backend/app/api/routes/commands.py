from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.api.schemas.requests import CreateCommandRequest, UpdateCommandRequest
from app.api.schemas.responses import CommandItem, CommandResponse, CommandsResponse, DeleteCommandResponse
from app.database.dal import DAL
from app.database.enums import CommandStatus
from app.database.repositories import CommandHistoryRepository, CommandsRepository

commands_router = APIRouter(tags=["Commands"])

CommandsRepo = Annotated[CommandsRepository, Depends(DAL.get_repo(DAL.commands))]
CommandHistoryRepo = Annotated[CommandHistoryRepository, Depends(DAL.get_repo(DAL.command_history))]


@commands_router.get("/")
async def get_commands(commands: CommandsRepo) -> CommandsResponse:
    """
    Retrieve all commands from the database.

    :param commands: injected Command repository.
    :return: All command entries.
    """
    return CommandsResponse(data=[CommandItem.model_validate(command) for command in await commands.get_all()])


@commands_router.get("/{command_id}")
async def get_command(command_id: UUID, commands: CommandsRepo) -> CommandResponse:
    """
    Retrieve a single command by ID.

    :param command_id: UUID of the command to retrieve.
    :param commands: injected Command repository.
    :return: The matching command entry.
    """
    try:
        command = await commands.get_by_id(command_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return CommandResponse(data=CommandItem.model_validate(command))


@commands_router.post("/")
async def create_command(
    request: CreateCommandRequest, commands: CommandsRepo, history_repo: CommandHistoryRepo
) -> CommandResponse:
    """
    Create a new command entry with status set to pending.

    :param request: Typed fields identifying the command type, session, and optional parameters.
    :param commands: injected Command repository.
    :return: The newly created command.
    """

    # TODO: (STEP 4) Wire CommandHistory table appending into this route!

    # history_repo = DAL.get_repo(DAL.command_history)()

    created_command = await commands.create(
        {
            "type_": request.type_,
            "params": request.params,
        }
    )

    await history_repo.create(
        {
            "command_id": created_command.id,
            # "type_": request.type_,
            "params": request.params,
            "status": CommandStatus.PENDING,
        }
    )

    return CommandResponse(data=CommandItem.model_validate(created_command))


@commands_router.patch("/{command_id}")
async def update_command(
    command_id: UUID, request: UpdateCommandRequest, commands: CommandsRepo, history_repo: CommandHistoryRepo
) -> CommandResponse:
    """
    Partially update a command's status, type, or parameters.

    :param command_id: UUID of the command to update.
    :param request: Fields to overwrite; omitted fields are left unchanged.
    :param commands: injected Command repository.
    :return: The updated command entry.
    :raises HTTPException: 404 if the command does not exist.
    :raises HTTPException: 422 if the repository rejects the update, e.g. a value of the wrong type or a
        ``type_`` that is not an existing main command. A rejected update leaves the command unchanged.
    """
    # get command
    try:
        cur_command = await commands.get_by_id(command_id)  # type SQLModel
    except Exception as err:
        raise HTTPException(status_code=404, detail="command not found") from err

    # update command
    try:
        updates = request.model_dump(exclude_none=True, exclude_unset=True)
        for field, value in updates.items():
            setattr(cur_command, field, value)

        updated_command = await commands.update(command_id, updates)
    except Exception as err:
        raise HTTPException(status_code=422) from err

    # TODO: (STEP 3) Implement this stub!

    # history_repo = DAL.get_repo(DAL.command_history)()
    await history_repo.create(
        {
            "command_id": command_id,
            "status": updated_command.status,
            # "type_": updated_command.type_,
            "params": updated_command.params,
        }
    )

    # TODO: (STEP 4) Wire CommandHistory table appending into this route!
    return CommandResponse(data=CommandItem.model_validate(cur_command))


@commands_router.delete("/{command_id}")
async def delete_command(
    command_id: UUID, commands: CommandsRepo, history_repo: CommandHistoryRepo
) -> DeleteCommandResponse:
    """
    Delete a command by ID.

    :param command_id: UUID of the command to delete.
    :param commands: injected Command repository.
    :return: Confirmation message with the deleted command ID.
    """
    # TODO: (STEP 4) Wire CommandHistory table appending into this route!

    # history_repo = DAL.get_repo(DAL.command_history)()

    try:
        cur_command = await commands.get_by_id(command_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    await history_repo.create(
        {
            "command_id": command_id,
            "status": cur_command.status,
            # "type_": cur_command.type_,
            "params": cur_command.params,
        }
    )

    await commands.delete_by_id(command_id)
    return DeleteCommandResponse(message=f"Command {command_id} deleted successfully")
