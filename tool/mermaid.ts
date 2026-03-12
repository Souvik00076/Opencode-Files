import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Generate diagram images from Mermaid text notation. Supports flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, gantt charts, and more. Returns the path to the generated image file.",
  args: {
    mermaid_text: tool.schema.string().describe("Mermaid diagram text notation (e.g., 'graph TD; A-->B; B-->C;')"),
    output_path: tool.schema.string().optional().describe("Optional output file path (defaults to ~/Downloads/mermaid_diagram.png)"),
    format: tool.schema.enum(['png', 'svg', 'pdf']).optional().default('png').describe("Output format: png, svg, or pdf"),
    theme: tool.schema.enum(['default', 'forest', 'dark', 'neutral']).optional().default('default').describe("Mermaid theme: default, forest, dark, or neutral"),
    background: tool.schema.string().optional().default('white').describe("Background color: transparent, white, or any CSS color")
  },
  async execute(args) {
    const scriptPath = `${process.env.HOME}/.config/opencode/tool/generate_mermaid.py`
    
    // Build command arguments
    const cmdArgs = [
      args.mermaid_text,
      args.output_path || '',
      args.format || 'png',
      args.theme || 'default',
      args.background || 'white'
    ]
    
    try {
      // Execute the Python script
      const result = await Bun.$`python3 ${scriptPath} ${cmdArgs[0]} ${cmdArgs[1]} ${cmdArgs[2]} ${cmdArgs[3]} ${cmdArgs[4]}`.text()
      
      // Parse JSON response
      const response = JSON.parse(result.trim())
      
      if (response.success) {
        return `✓ ${response.message}\n\nYou can view the diagram at: ${response.output_path}`
      } else {
        return `✗ Error: ${response.error}`
      }
    } catch (error) {
      return `✗ Failed to generate diagram: ${error}`
    }
  }
})
