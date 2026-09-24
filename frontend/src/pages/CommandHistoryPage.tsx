import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";
import { useState } from "react";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  // TODO: (STEP 8) Define the columns needed for the CommandHistory table.
  columnHelper.accessor("id", { header: "ID" }),
  columnHelper.accessor("command_id", { header: "Command ID" }),
  columnHelper.accessor("status", { header: "Status" }),
  columnHelper.accessor("params", { header: "Params" }),
  columnHelper.accessor("created_at", { header: "Created at" }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [commandId, setCommandId] = useState<string>("");

  const { data: history } = useCommandHistory(commandId);

  // TODO: (STEP 8) Fetch the command history with useCommandHistory and pass the resulting
  // CommandHistory[] directly to the Table component.
  //
  // The page must provide a way for the user to select which command's audit log they want to view.
  // The selected command should determine which command history is fetched.
  // The table should communicate that this is an audit log.
  // The table should be centred on the page.
  return (
    <div className="flex flex-col items-center justify-center">
      <div>
        <SetCommandIdButton setCommandId={setCommandId} />
      </div>
      <div>
        <div>Command ID: {commandId}</div>
        <Table data={history == undefined ? [] : history} columns={columns} />
      </div>
    </div>
  );
}

export default CommandHistoryPage;

type SetCommandIdButtonProps = {
  setCommandId: (commandId: string) => void;
};
function SetCommandIdButton({ setCommandId }: SetCommandIdButtonProps) {
  const [commandId, setCommandIdLocal] = useState<string>("");
  return (
    <div className="border b-4 border-blue-800 rounded-md p-3">
      <input
        type="text"
        className="border b-2 p-1 w-100 rounded-md bg-gray-900 text-lg"
        value={commandId}
        onChange={(e) => setCommandIdLocal(e.target.value)}
        placeholder="Enter command ID"
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            setCommandId(commandId);
          }
        }}
      />
      <button
        className="border b-2 p-1 bg-blue-600 hover:bg-blue-700 transition text-lg rounded-md"
        onClick={() => setCommandId(commandId)}
      >
        View Command
      </button>
    </div>
  );
}
