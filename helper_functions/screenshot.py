import asyncio
import os
from playwright.async_api import async_playwright
from PIL import Image # Import Pillow

async def take_and_split_screenshot(url, base_output_path="screenshot"):
    """
    Navigates to a URL, takes a full-page screenshot, and splits it
    into multiple images based on viewport height.

    Args:
        url (str): The URL of the webpage to capture.
        base_output_path (str): The base name for the output image files
                                 (e.g., 'page_screenshot'). Chunks will be
                                 saved as 'base_output_path_part_N.png'.

    Returns:
        list: A list of file paths for the generated image chunks.
              Returns an empty list if an error occurs.
    """
    output_paths = []
    # Ensure the base path doesn't end with an extension for easier concatenation
    base_name = os.path.splitext(base_output_path)[0]
    full_screenshot_path = f"{base_name}_full.png" # Temporary path for the full screenshot

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="networkidle")

            # --- Take the full screenshot ---
            print(f"Taking full screenshot and saving temporarily to {full_screenshot_path}...")
            await page.screenshot(path=full_screenshot_path, full_page=True)
            print("Full screenshot saved.")

            # --- Get viewport height for splitting ---
            viewport_size = page.viewport_size # Returns {'width': w, 'height': h}
            if not viewport_size:
                 # Fallback if viewport_size is None (less likely but possible)
                 # You might want to set a default or raise an error
                 print("Warning: Could not determine viewport size. Using default height 800px.")
                 viewport_height = 800
            else:
                viewport_height = viewport_size['height']
            print(f"Using viewport height for splitting: {viewport_height}px")

            # --- Split the screenshot ---
            print("Splitting the screenshot into chunks...")
            img = Image.open(full_screenshot_path)
            img_width, img_height = img.size

            # Calculate number of chunks needed (ceiling division)
            num_chunks = (img_height + viewport_height - 1) // viewport_height

            for i in range(num_chunks):
                # Define the box for cropping (left, upper, right, lower)
                top = i * viewport_height
                # Ensure the bottom coordinate doesn't exceed the image height
                bottom = min((i + 1) * viewport_height, img_height)
                box = (0, top, img_width, bottom)

                # Crop the image
                chunk = img.crop(box)

                # Save the chunk
                chunk_path = f"{base_name}_part_{i+1}.png"
                chunk.save(chunk_path)
                output_paths.append(chunk_path)
                print(f"Saved chunk {i+1} to {chunk_path}")

            img.close() # Close the image file
            print("Screenshot splitting complete.")

        except Exception as e:
            print(f"An error occurred: {e}")
            output_paths = [] # Clear paths on error

        finally:
            # Clean up the temporary full screenshot
            if os.path.exists(full_screenshot_path):
                try:
                    os.remove(full_screenshot_path)
                    print(f"Removed temporary file: {full_screenshot_path}")
                except OSError as e:
                    print(f"Error removing temporary file {full_screenshot_path}: {e}")
            if 'browser' in locals() and browser.is_connected():
                await browser.close()

    return output_paths

# # --- How to use it ---
# if __name__ == "__main__":
#     target_url = "https://arxiv.org/abs/2404.04671"

#     screenshots_dir = "screenshots"
#     os.makedirs(screenshots_dir, exist_ok=True)

#     output_base_name = os.path.join(screenshots_dir, "screenshot")

#     # Run the async function
#     created_files = asyncio.run(take_and_split_screenshot(target_url, output_base_name))

#     if created_files:
#         print("\nSuccessfully created screenshot chunks:")
#         for f in created_files:
#             print(f"- {f}")
#     else:
#         print("\nScreenshot generation failed or produced no files.")