from slide_generator import SlideGenerator
import os

def test_generation():
    print("Testing PPTX generation...")
    
    data = {
        "title": "Test Presentation",
        "slides": [
            {
                "title": "Slide 1",
                "content": ["Point A", "Point B"],
                "speaker_notes": "Note 1"
            },
            {
                "title": "Slide 2",
                "content": ["Point C", "Point D"]
            }
        ]
    }
    
    generator = SlideGenerator()
    output = generator.create_presentation(data, "test_output.pptx")
    
    if os.path.exists(output):
        print(f"Success! File created at {output}")
    else:
        print("Failed to create file.")

if __name__ == "__main__":
    test_generation()
