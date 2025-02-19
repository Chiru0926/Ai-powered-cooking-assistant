"use client"

import { useState, useEffect } from "react"

interface NutrientInfo {
  ingredient: string
  country: string
  state: string
  nutrients: Record<string, number>
}

export default function NutritionInfo() {
  const [nutritionInfo, setNutritionInfo] = useState<NutrientInfo[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch("/api/nutrition")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        return res.json()
      })
      .then((data) => setNutritionInfo(data))
      .catch((e) => {
        console.error("Failed to fetch nutrition info:", e)
        setError("Failed to load nutrition information. Please try again later.")
      })
  }, [])

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  return (
    <div className="space-y-4">
      {nutritionInfo.map((info, index) => (
        <div key={index} className="bg-gray-100 p-4 rounded">
          <h3 className="text-lg font-semibold">{info.ingredient}</h3>
          <p className="text-sm text-gray-600">
            Origin: {info.country}, {info.state}
          </p>
          <ul className="mt-2">
            {Object.entries(info.nutrients).map(([nutrient, value]) => (
              <li key={nutrient} className="text-sm">
                {nutrient}: {value}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

