import cv2
import easyocr
import os 

IMAGE_PATH = 'C:\\Users\\zhaoy\\Desktop\\IoT\\HMI OCR\\HMI_Data.jpg'
CONFIDENCE_THRESHOLD = 0.4

reader = easyocr.Reader(['en'], gpu=False)

def test_ocr_function():
    # 1. Check if image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"ERROR: Image not found at {IMAGE_PATH}")
        print("Please place 'latest.jpg' in the same folder as this script.")
        return

    print(f"Loading image: {IMAGE_PATH}...")
    
    # 2. Initialize EasyOCR Reader
    # 'gpu=True' is faster if you have an NVIDIA card. 
    # If not, it will automatically fallback to CPU (but prints a warning).
    print("Initializing AI Model (this takes a moment)...")
    reader = easyocr.Reader(['en'], gpu=False) 

    # 3. Perform OCR
    # detail=1 gives us the text AND the location (bounding box)
    print("Reading text...")
    results = reader.readtext(IMAGE_PATH, detail=1)

    # 4. Process and Visualize Results
    img = cv2.imread(IMAGE_PATH)
    captured_text = []

    print("\n" + "="*40)
    print("       RAW DETECTION RESULTS")
    print("="*40)

    for (bbox, text, prob) in results:
        # bbox is the coordinates of the box corners
        # prob is the probability (confidence) score
        
        if prob >= CONFIDENCE_THRESHOLD:
            print(f"[CONFIDENCE: {prob:.2f}] Detected: '{text}'")
            captured_text.append(text)
            
            # --- VISUALIZATION (Draw box on image) ---
            # Extract corner points to draw the rectangle 
            # bbox format: top left [0], top right [1], bottom right [2], bottom left [3]

            # Use map to apply integer function (usually bbox is a float)
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            
            # Draw green rectangle
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            
            # Write detected text above the box
            cv2.putText(img, text, (top_left[0], top_left[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            print(f"[SKIPPED] Low confidence ({prob:.2f}): '{text}'")

    # 5. Final Output
    final_string = " ".join(captured_text)
    print("="*40)
    print(f"\nFINAL READOUT: {final_string}")
    print("="*40)

    # 6. Show the image with boxes
    # This will open a popup window showing exactly what the AI saw.
    # Press any key to close the window.
    cv2.imshow('EasyOCR Debug View', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Optional: Save the debug image
    cv2.imwrite('debug_result.jpg', img)
    print("Debug image saved as 'debug_result.jpg'")

if __name__ == "__main__":
    test_ocr_function()