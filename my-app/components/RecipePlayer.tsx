"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function RecipePlayer() {
  const [recipeIndex, setRecipeIndex] = useState("")
  const [playerState, setPlayerState] = useState<"idle" | "playing" | "paused">("idle")

  const handlePlay = async () => {
    const response = await fetch(`/api/recipe-audio?index=${recipeIndex}`, { method: "POST" })
    if (response.ok) {
      setPlayerState("playing")
    }
  }

  const handlePause = async () => {
    const response = await fetch("/api/recipe-audio?action=pause", { method: "POST" })
    if (response.ok) {
      setPlayerState("paused")
    }
  }

  const handleResume = async () => {
    const response = await fetch("/api/recipe-audio?action=resume", { method: "POST" })
    if (response.ok) {
      setPlayerState("playing")
    }
  }

  const handleStop = async () => {
    const response = await fetch("/api/recipe-audio?action=stop", { method: "POST" })
    if (response.ok) {
      setPlayerState("idle")
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex space-x-2">
        <Input
          type="number"
          placeholder="Enter dish number"
          value={recipeIndex}
          onChange={(e) => setRecipeIndex(e.target.value)}
          className="w-40"
        />
        <Button onClick={handlePlay} disabled={playerState !== "idle"}>
          Play
        </Button>
      </div>
      <div className="space-x-2">
        <Button onClick={handlePause} disabled={playerState !== "playing"}>
          Pause
        </Button>
        <Button onClick={handleResume} disabled={playerState !== "paused"}>
          Resume
        </Button>
        <Button onClick={handleStop} disabled={playerState === "idle"}>
          Stop
        </Button>
      </div>
    </div>
  )
}

