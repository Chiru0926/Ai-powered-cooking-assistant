import { NextResponse } from "next/server"
import fs from "fs"
import path from "path"
import { process } from "fuzzywuzzy"

function readIngredients(filePath: string): string[] {
  return fs
    .readFileSync(filePath, "utf-8")
    .split(",")
    .map((i) => i.trim().toLowerCase())
}

function readRecipes(filePath: string): Record<string, string[]> {
  const recipes: Record<string, string[]> = {}
  const content = fs.readFileSync(filePath, "utf-8")
  const rows = content.split("\n")
  for (const row of rows) {
    const [dish, ...ingredients] = row.split(",").map((i) => i.trim())
    recipes[dish] = ingredients
  }
  return recipes
}

function suggestDishes(availableIngredients: string[], recipes: Record<string, string[]>) {
  const suggestedDishes = []

  for (const [dish, ingredients] of Object.entries(recipes)) {
    const matchCount = ingredients.reduce((count, ing) => {
      const match = process.extractOne(ing, availableIngredients)
      return match && match[1] > 80 ? count + 1 : count
    }, 0)
    const matchPercentage = (matchCount / ingredients.length) * 100

    if (matchPercentage > 70) {
      suggestedDishes.push({ dish, matchPercentage })
    }
  }

  return suggestedDishes.sort((a, b) => b.matchPercentage - a.matchPercentage)
}

export async function GET() {
  const ingredientsPath = path.join(process.cwd(), "ing.txt")
  const recipesPath = path.join(process.cwd(), "Dish.csv")

  const userIngredients = readIngredients(ingredientsPath)
  const recipes = readRecipes(recipesPath)

  const suggestions = suggestDishes(userIngredients, recipes)

  return NextResponse.json(suggestions)
}

