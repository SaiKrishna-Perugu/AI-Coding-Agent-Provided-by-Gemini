import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info

def  main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("I need a prompt....!")
        sys.exit(2)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    print(response.text)
    if response is None or response.usage_metadata is None:
       return
    if verbose:

        print(f"User prompt: {prompt}") 
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") 
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()