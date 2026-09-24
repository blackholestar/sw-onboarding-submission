import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  // TODO: (STEP 7) Implement this hook.
  // This hook should use React Query and return CommandHistory[].
  // Define the refetch interval as a local constant.

  return useQuery({
    queryKey: ["command-history", commandId],
    queryFn: async () => {
      const response = await fetch(`/api/commands/${commandId}/history`, {
        cache: "no-store",
      });

      if (!response.ok) {
        throw Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      return data.data as CommandHistory[];
    },
    refetchInterval: 2000,
    enabled: commandId !== "",
  });

  //throw new Error("not implemented");
}

/*
async function addChallenge(completedChallenge: Challenge | null) {
    const response = await fetch(`/api/game/${gameId}/add-challenge`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        completedChallenge
      })
    });
    const data = await response.json();

    console.log(data);
    setGameState(data.newGameState);

  }

import {gameManager} from "@/server/GameManager";

export async function POST(request: Request, { params }: { params: Promise<{ gameId: string }> }) {
    const {completedChallenge} = await request.json();
    const { gameId } = await params;
    const response = await gameManager.addChallenge(gameId, completedChallenge);
    if (!response.success) {
        return Response.json(response, {status: 409});
    }
    return Response.json(response);
}
*/
