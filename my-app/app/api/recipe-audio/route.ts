import { NextResponse } from "next/server"
import fs from "fs"
import path from "path"
import { TTSController } from "@/lib/ttsController"

let ttsController: TTSController | null = null

export async function POST(request: Request) {
  const { searchParams } = new URL(request.url)
  const index = searchParams.get("index")
  const action = searchParams.get("action")

  if (action) {
    if (!ttsController) {
      return NextResponse.json({ error: "No active audio playback" }, { status: 400 })
    }

    switch (action) {
      case "pause":
        ttsController.pause()
        break
      case "resume":
        ttsController.resume()
        break
      case "stop":
        ttsController.stop()
        ttsController = null
        break
      default:
        return NextResponse.json({ error: "Invalid action" }, { status: 400 })
    }

    return NextResponse.json({ success: true })
  }

  if (!index) {
    return NextResponse.json({ error: "Missing recipe index" }, { status: 400 })
  }

  const recipesPath = path.join(process.cwd(), "Dish.csv")
  const recipes = fs.readFileSync(recipesPath, "utf-8").split("\n")

  const recipeIndex = Number.parseInt(index) - 1
  if (recipeIndex < 0 || recipeIndex >= recipes.length) {
    return NextResponse.json({ error: "Invalid recipe index" }, { status: 400 })
  }

  const recipe = recipes[recipeIndex].split(",")
  const recipeText = `Recipe for ${recipe[0]}: ${recipe.slice(1, 4).join(", ")}`

  if (ttsController) {
    ttsController.stop()
  }

  ttsController = new TTSController()
  ttsController.speak(recipeText)

  return NextResponse.json({ success: true })
}

