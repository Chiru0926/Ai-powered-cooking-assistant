import { spawn } from "child_process"
import fs from "fs"
import path from "path"

export class TTSController {
  private process: any
  private audioFile: string

  constructor() {
    this.audioFile = path.join(process.cwd(), "temp_audio.mp3")
  }

  speak(text: string) {
    const pythonScript = path.join(process.cwd(), "recipe.py")
    this.process = spawn("python", [pythonScript, text])

    this.process.stdout.on("data", (data: Buffer) => {
      console.log(`Python script output: ${data}`)
    })

    this.process.stderr.on("data", (data: Buffer) => {
      console.error(`Python script error: ${data}`)
    })
  }

  pause() {
    if (this.process) {
      this.process.stdin.write("pause\n")
    }
  }

  resume() {
    if (this.process) {
      this.process.stdin.write("resume\n")
    }
  }

  stop() {
    if (this.process) {
      this.process.stdin.write("stop\n")
      this.process.kill()
      this.process = this.process.stdin.write("stop\n")
      this.process.kill()
      this.process = null
    }

    if (fs.existsSync(this.audioFile)) {
      fs.unlinkSync(this.audioFile)
    }
  }
}

