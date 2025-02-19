"use client"

import { useState, useEffect } from "react"

interface Recipe {
  name: string
  match: number
}

export default function RecipeList() {
  const [recipes, setRecipes] = useState<Recipe[]>([])

  useEffect(() => {
    fetch("/api/recipes")
      .then((res) => res.json())
      .then((data) => setRecipes(data))
  }, [])

  return (
    <ul className="space-y-2">
      {recipes.map((recipe, index) => (
        <li key={index} className="bg-gray-100 p-2 rounded">
          <span className="font-semibold">{recipe.name}</span>
          <span className="ml-2 text-sm text-gray-600">({recipe.match.toFixed(1)}% match)</span>
        </li>
      ))}
    </ul>
  )
}

