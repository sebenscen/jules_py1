import google.generativeai as genai
import os
import json # For potential parsing if the response is a JSON string

# It's good practice to configure the API key early,
# though often it's done right before the first API call.
# Assuming GOOGLE_API_KEY is set in the environment.
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # This might be better inside the function or guarded

def get_inspirational_phrase():
    """
    Generates an inspirational phrase using the Gemini API.

    Returns:
        dict: A dictionary containing 'phrase', 'author', and 'location',
              or None if an error occurs.
    """
    try:
        # Configure API key. It's safer to do it here if the module might be imported
        # without the key being configured globally yet.
        # However, the prompt states "assume the API key is handled by the library's
        # environment variable setup", which implies genai.configure() might not be strictly needed
        # if the library picks it up automatically from os.environ["GOOGLE_API_KEY"].
        # For robustness, explicitly configuring can be good.
        # Let's try without explicit configure first, as per problem statement implication.
        
        model = genai.GenerativeModel('gemini-pro') # Or other suitable model

        prompt = (
            "Generate a short inspirational phrase. "
            "Also provide the author of the phrase and the author's primary known location "
            "(e.g., city or country of birth, or primary place of work if very well-known). "
            "Format the output as a JSON object with three keys: 'phrase', 'author', and 'location'. "
            "For example: {\"phrase\": \"The only way to do great work is to love what you do.\", \"author\": \"Steve Jobs\", \"location\": \"San Francisco\"}. "
            "If the location is not applicable or widely known for a common phrase/author, use null for location."
        )

        response = model.generate_content(prompt)
        
        # Assuming the response text will be a JSON string as requested.
        # Need to handle potential issues with response.text or response.parts
        if response.parts:
            # Assuming the first part contains the text.
            # The response might not always be simple text, check documentation for complex responses.
            content_text = response.text # or response.parts[0].text if .text is not directly available or suitable
        else:
            # This case might occur if the response was blocked or had no content.
            print("Error: Empty response from API.")
            return None

        # Parse the JSON response
        data = json.loads(content_text)
        
        # Basic validation, though the prompt asks for specific keys.
        if not all(key in data for key in ['phrase', 'author', 'location']):
             print(f"Error: API response missing expected keys. Response: {content_text}")
             return None

        return {
            "phrase": data.get("phrase"),
            "author": data.get("author"),
            "location": data.get("location") # This can be None as per prompt
        }

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON response from API. Response: {content_text}")
        return None
    except Exception as e:
        # This will catch other errors, like connection issues, API key problems, etc.
        print(f"An error occurred: {e}")
        # Consider if specific exceptions from the genai library should be caught.
        # e.g., google.auth.exceptions.DefaultCredentialsError if API key is missing/invalid
        # or genai.types.generation_types.BlockedPromptException etc.
        return None

if __name__ == '__main__':
    # Example usage (optional, for testing)
    # Make sure GOOGLE_API_KEY is set in your environment to test this directly
    # For example: export GOOGLE_API_KEY="your_api_key_here"
    # result = get_inspirational_phrase()
    # if result:
    #     print(f"Phrase: {result['phrase']}")
    #     print(f"Author: {result['author']}")
    #     print(f"Location: {result['location']}")
    # else:
    #     print("Failed to get inspirational phrase.")
    pass # Keep the __main__ block minimal for a library file.
