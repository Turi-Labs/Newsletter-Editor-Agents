import asyncio
import os
from playwright.async_api import async_playwright
from PIL import Image # Import Pillow

async def take_and_split_screenshot(url, base_output_path="screenshot", mobile=True, timeout=60000):
    output_paths = []
    base_name = os.path.splitext(base_output_path)[0]
    full_screenshot_path = f"{base_name}_full.png"

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={"width": 375, "height": 812},
                device_scale_factor=2.0,
                is_mobile=mobile,
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1" if mobile else None
            )
            page = await context.new_page()

            print(f"Navigating to {url} in {'mobile' if mobile else 'desktop'} mode...")
            try:
                # First try with networkidle but with increased timeout
                await page.goto(url, wait_until="networkidle", timeout=timeout)
            except Exception as e:
                print(f"Warning: networkidle timeout ({e}). Falling back to load event...")
                # If networkidle times out, fall back to just waiting for the load event
                await page.goto(url, wait_until="load", timeout=timeout)
                # Give a little extra time for any remaining resources
                await page.wait_for_timeout(2000)

            print(f"Taking full screenshot and saving temporarily to {full_screenshot_path}...")
            await page.screenshot(path=full_screenshot_path, full_page=True)
            print("Full screenshot saved.")

            # Get viewport height for splitting
            viewport_size = page.viewport_size
            viewport_height = viewport_size['height'] if viewport_size else 812
            print(f"Using viewport height for splitting: {viewport_height}px")

            # Split the screenshot
            print("Splitting the screenshot into chunks...")
            img = Image.open(full_screenshot_path)
            img_width, img_height = img.size

            num_chunks = (img_height + viewport_height - 1) // viewport_height

            for i in range(num_chunks):
                top = i * viewport_height
                bottom = min((i + 1) * viewport_height, img_height)
                box = (0, top, img_width, bottom)

                chunk = img.crop(box)
                chunk_path = f"{base_name}_part_{i+1}.png"
                chunk.save(chunk_path)
                output_paths.append(chunk_path)
                print(f"Saved chunk {i+1} to {chunk_path}")

            img.close()

            # Clean up the temporary full screenshot
            try:
                os.remove(full_screenshot_path)
                print(f"Removed temporary file {full_screenshot_path}")
            except:
                print(f"Warning: Could not remove temporary file {full_screenshot_path}")

            print("Screenshot splitting complete.")
            return output_paths

        except Exception as e:
            print(f"An error occurred: {e}")
            # Try to clean up the temporary file if it exists
            try:
                if os.path.exists(full_screenshot_path):
                    os.remove(full_screenshot_path)
            except:
                pass
            return []

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
if __name__ == "__main__":
    target_url = "https://openai.com/global-affairs/openai-for-countries/"

    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    output_base_name = os.path.join(screenshots_dir, "screenshot")

    # Run the async function
    created_files = asyncio.run(take_and_split_screenshot(target_url, output_base_name))

    if created_files:
        print("\nSuccessfully created screenshot chunks:")
        for f in created_files:
            print(f"- {f}")
    else:
        print("\nScreenshot generation failed or produced no files.")