import { NextResponse } from "next/server"
import fs from "fs"
import path from "path"

export async function GET() {
  const ingredientsPath = path.join(process.cwd(), "ing.txt")
  const ingredients = fs
    .readFileSync(ingredientsPath, "utf-8")
    .split(",")
    .map((i) => i.trim())
  return NextResponse.json(ingredients)
}

