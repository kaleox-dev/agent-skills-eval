#!/usr/bin/env python3
"""
Debug script to test gpt-5.5's JSON output compliance.
Saves the raw response to judge_debug.jsonl in the target folder.
DO NOT RUN THIS AUTOMATICALLY.
"""
import os
import sys
import json
import openai
from pathlib import Path

def main():
    # 1. Check API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable is not set.")
        print("   Run: export OPENAI_API_KEY='your-key'")
        sys.exit(1)

    # 2. Parse Arguments
    if len(sys.argv) < 2:
        print("❌ Usage: python3 debug_judge.py <output-folder>")
        print("   Example: python3 debug_judge.py eval-results/gpt5.5-ab-testing")
        sys.exit(1)

    target_folder = Path(sys.argv[1])
    if not target_folder.exists():
        print(f"❌ Error: Folder '{target_folder}' does not exist.")
        sys.exit(1)

    # 3. Setup Client
    client = openai.OpenAI(api_key=api_key)

    # 4. Define the Test Prompt (Simulating what the runner does)
    # We use a strict system prompt and a simple task to test JSON compliance.
    test_prompt = "The model output was: 'Probably not yet.' Does this address the peeking problem? Output ONLY valid JSON: {\"pass\": true/false, \"evidence\": \"string\"}"
    
    print(f"🔍 Testing gpt-5.5 on folder: {target_folder}")
    print("📡 Sending request to gpt-5.5 with temperature=0 and response_format=json_object...")

    try:
        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a strict JSON validator. You must output ONLY valid JSON. No markdown, no code blocks, no explanations. If you cannot determine the answer, output {\"error\": \"insufficient data\"}."
                },
                {
                    "role": "user", 
                    "content": test_prompt
                }
            ],
            temperature=0.0,              # CRITICAL: Forces deterministic output
            response_format={"type": "json_object"} # CRITICAL: Forces JSON mode
        )

        raw_content = response.choices[0].message.content
        model_id = response.model

        print("\n✅ Raw Response Received:")
        print("-" * 40)
        print(raw_content)
        print("-" * 40)

        # 5. Save to File
        debug_file = target_folder / "judge_debug.jsonl"
        debug_entry = {
            "model": model_id,
            "prompt": test_prompt,
            "raw_response": raw_content,
            "timestamp": str(os.popen("date").read().strip())
        }

        with open(debug_file, "w") as f:
            f.write(json.dumps(debug_entry) + "\n")

        print(f"\n💾 Saved raw response to: {debug_file}")
        print("   Open this file to see if the model included markdown (```json) or extra text.")

    except Exception as e:
        print(f"\n❌ API Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
