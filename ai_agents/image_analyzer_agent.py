from openai import OpenAI
import os
import yaml
import base64
from dotenv import load_dotenv

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def load_prompts():
    try:
        with open('prompts/image_analyzer_agent.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise Exception("prompts.yaml file not found")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing YAML file: {e}")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
prompts = load_prompts()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def image_analyzer(images_path: list[str], tweet: str) -> str:
    # Construct the prompt content
    content = [
        {"type": "text", "text": prompts['task']['description'].format(images_path=images_path, tweet=tweet)},
        {"type": "text", "text": f"\n\nTweet to analyze: {tweet}"},
        {"type": "text", "text": f"\n\nExpected Output Format: {prompts['task']['expected_output']}"}
    ]

    # Add images to the content
    # Only process up to 5 images
    for image_path in images_path[:3]:
        try:
            # Getting the base64 string
            base64_image = encode_image(image_path)
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}" # Assuming PNG, adjust if needed
                    }
                }
            )
        except FileNotFoundError:
            print(f"Warning: Image file not found at {image_path}. Skipping this image.")
            continue
        except Exception as e:
            print(f"Warning: Could not process image {image_path}: {e}. Skipping this image.")
            continue

    # Define the system prompt based on agent details
    system_prompt = f"""Role: {prompts['agent']['role']}
    Goal: {prompts['agent']['goal']}
    Backstory: {prompts['agent']['backstory']}
    """

    try:
        response = client.chat.completions.create(
            # model="gpt-4-vision-preview", # Or "gpt-4o" or "gpt-4o-mini"
            model="gpt-4o-mini", # Using o-mini as potentially more cost-effective
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_tokens=500, # Adjust as needed
            temperature=0.8, # Match original temperature if desired
            # stop=["END"] # Stop sequences if needed
        )
        result = response.choices[0].message.content
        print(result)
        return result

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error during analysis: {e}"

# # Example Usage:
# tweet = """The study infers LLM relationships by comparing outputs from many prompts,
# hinting that training data may shape model similarities more than architecture.
# It feels like we're seeing models reveal their own backstories through their responses."""

# images_path=["screenshots/screenshot_part_1.png", "screenshots/screenshot_part_2.png"]

# analysis_result = image_analyzer(images_path=images_path, tweet=tweet)
