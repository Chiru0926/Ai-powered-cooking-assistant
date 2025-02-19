"use client"

import { useState, useEffect } from "react"

export default function IngredientList() {
  const [ingredients, setIngredients] = useState<string[]>([])

  useEffect(() => {
    fetch("/api/ingredients")
      .then((res) => res.json())
      .then((data) => setIngredients(data))
  }, [])

  return (
    <ul className="list-disc pl-5">
      {ingredients.map((ingredient, index) => (
        <li key={index}>{ingredient}</li>
      ))}
    </ul>
  )
}

