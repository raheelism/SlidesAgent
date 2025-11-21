from bing_image_downloader import downloader
import os
import shutil

def test_bing(query):
    print(f"Testing Bing for: {query}")
    try:
        # Download to a temp directory
        output_dir = "temp_images"
        downloader.download(query, limit=1,  output_dir=output_dir, adult_filter_off=True, force_replace=False, timeout=10, verbose=True)
        
        # Check if image exists
        dir_path = os.path.join(output_dir, query)
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            if files:
                print(f"Found image: {files[0]}")
                return True
            else:
                print("No files found in directory.")
        else:
            print("Directory not created.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if os.path.exists("temp_images"):
            shutil.rmtree("temp_images", ignore_errors=True)

if __name__ == "__main__":
    test_bing("Artificial Intelligence")
