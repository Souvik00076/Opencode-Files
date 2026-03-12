#!/usr/bin/env python3
"""
Mermaid Diagram Generator
Converts Mermaid text to diagram images using mermaid-cli (mmdc)
"""

import sys
import subprocess
import os
import tempfile
import json
from pathlib import Path


def generate_mermaid_diagram(mermaid_text, output_path=None, format='png', theme='default', background='white'):
    """
    Generate a diagram from Mermaid text
    
    Args:
        mermaid_text: Mermaid diagram text
        output_path: Output file path (optional, generates temp file if not provided)
        format: Output format (png, svg, pdf)
        theme: Mermaid theme (default, forest, dark, neutral)
        background: Background color (transparent, white, or any CSS color)
    
    Returns:
        Path to the generated diagram file
    """
    
    # Check if mmdc is installed
    try:
        subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return json.dumps({
            "success": False,
            "error": "mermaid-cli (mmdc) is not installed. Install it with: npm install -g @mermaid-js/mermaid-cli"
        })
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_input:
        temp_input.write(mermaid_text)
        input_file = temp_input.name
    
    try:
        # Generate output path if not provided
        if output_path is None:
            output_dir = Path.home() / 'Downloads'
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f'mermaid_diagram.{format}'
        else:
            output_path = Path(output_path)
        
        # Build mmdc command
        cmd = [
            'mmdc',
            '-i', input_file,
            '-o', str(output_path),
            '-t', theme,
            '-b', background
        ]
        
        # Run mermaid-cli
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return json.dumps({
                "success": False,
                "error": f"Failed to generate diagram: {result.stderr}"
            })
        
        return json.dumps({
            "success": True,
            "output_path": str(output_path),
            "message": f"Diagram successfully generated at: {output_path}"
        })
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Error generating diagram: {str(e)}"
        })
    
    finally:
        # Clean up temporary input file
        try:
            os.unlink(input_file)
        except:
            pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python generate_mermaid.py <mermaid_text> [output_path] [format] [theme] [background]"
        }))
        sys.exit(1)
    
    mermaid_text = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    format = sys.argv[3] if len(sys.argv) > 3 else 'png'
    theme = sys.argv[4] if len(sys.argv) > 4 else 'default'
    background = sys.argv[5] if len(sys.argv) > 5 else 'white'
    
    result = generate_mermaid_diagram(mermaid_text, output_path, format, theme, background)
    print(result)
