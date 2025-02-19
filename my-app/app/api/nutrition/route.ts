import { NextResponse } from "next/server"
import fs from "fs"
import path from "path"

// Replace with your actual Edamam API credentials
const EDAMAM_APP_ID = process.env.EDAMAM_APP_ID
const EDAMAM_APP_KEY = process.env.EDAMAM_APP_KEY

function readIngredients(filePath: string): string[] {
  return fs
    .readFileSync(filePath, "utf-8")
    .split(",")
    .map((i) => i.trim().toLowerCase())
}

async function getNutrientInfo(ingredient: string) {
  try {
    const url = `https://api.edamam.com/api/food-database/v2/parser?ingr=${encodeURIComponent(ingredient)}&app_id=${EDAMAM_APP_ID}&app_key=${EDAMAM_APP_KEY}`
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    if ("parsed" in data && data.parsed.length > 0) {
      const food = data.parsed[0].food
      return food.nutrients || null
    }
    return null
  } catch (error) {
    console.error(`Error fetching nutrient info for ${ingredient}:`, error)
    return null
  }
}

function getGeographicalInfo(ingredient: string) {
  // This is a placeholder function. Replace with actual implementation.
  const geographicalInfo: Record<string, { country: string; state: string }> = {
    garlic: { country: "USA", state: "California" },
    butter: { country: "France", state: "Normandy" },
    // Add more ingredients and their geographical info here
  }
  return geographicalInfo[ingredient] || { country: "Unknown", state: "Unknown" }
}

export async function GET() {
  try {
    const ingredientsPath = path.join(process.cwd(), "ing.txt")
    const ingredients = readIngredients(ingredientsPath)

    const nutritionInfo = await Promise.all(
      ingredients.map(async (ingredient) => {
        const nutrientInfo = await getNutrientInfo(ingredient)
        const geographicalInfo = getGeographicalInfo(ingredient)

        return {
          ingredient: ingredient,
          country: geographicalInfo.country,
          state: geographicalInfo.state,
          nutrients: nutrientInfo,
        }
      }),
    )

    return NextResponse.json(nutritionInfo)
  } catch (error) {
    console.error("Error in nutrition API route:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}

