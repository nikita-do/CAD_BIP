#Libraries
import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob

# Suporting buffers
images = []

# Supporting functions
def update_image(index):
    global images
    originalImage = images[index];
    #Convert to 8-bit image
    normalizedImage = cv2.normalize(originalImage, None, 0, 255, cv2.NORM_MINMAX);
    uint8Image = np.uint8(normalizedImage);
    cv2.imshow('DICOM Image Sequence', uint8Image);

#Testing function
def testingReadingDICOMFile():
    #Initializing
    print("Initializing...")

    #Reading dicom file
    print("Reading dicom file...")
    dicom_files = sorted(glob.glob("../../Data/CAD_Data/dicom_lung/*.dcm"))
    global images
    images = [pydicom.dcmread(file).pixel_array for file in dicom_files];

    #Print the number of files loaded
    print(f"Loaded {len(images)} DICOM files")

    # Create a window and a trackbar
    cv2.namedWindow('DICOM Image Sequence')
    cv2.createTrackbar('Index', 'DICOM Image Sequence', 0, len(images) - 1, lambda x: update_image(x))

    # Display the first image
    update_image(0)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Main function
def mainFunction():
    print("Initializing...")

#Main program
def main():
    # Your main code goes here
    os.system("cls")
    testingReadingDICOMFile()
if __name__ == "__main__":
    main()