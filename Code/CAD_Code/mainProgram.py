#Libraries
import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.signal import wiener;

# Supporting functions
def region_growing(img, seed, threshold=10):
    segmented = np.zeros_like(img)
    stack = [seed]
    while stack:
        x, y = stack.pop()
        if segmented[x, y] == 0 and abs(int(img[x, y]) - int(img[seed])) < threshold:
            segmented[x, y] = 255
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < img.shape[0] and 0 <= y + dy < img.shape[1]:
                        stack.append((x + dx, y + dy))
    return segmented

#Testing function
def testingReadingDICOMFile():
    #Initializing
    print("Initializing...")

    #Reading dicom file
    print("Reading dicom file...")
    dicomFilePath = "../../Data/CAD_Data/dicom_lung/000004.dcm"
    dicomFile = pydicom.dcmread(dicomFilePath)
    originalImage = dicomFile.pixel_array;

    # Convert dicom file to opencv data
    print("Converting dicom data to pixel  ...");
    originalImage = np.array(originalImage);
    print("\tThe shape of pixelArray: ", originalImage.shape);
    normalizedImage = cv2.normalize(originalImage, None, 0, 255, cv2.NORM_MINMAX);
    uint8Image = np.uint8(normalizedImage);

    # Equalize the gray image
    print("Equalize the gray image ...");
    equalizedImage = cv2.equalizeHist(uint8Image);
    
    # Apply Gaussian and median Blur
    print("Blur the gray image ...");
    blurredImage_gaussian = cv2.GaussianBlur(equalizedImage, (11, 11), 0);
    blurredImage_median = cv2.medianBlur(equalizedImage, 15);

    # Apply unsharp masking to sharpen image
    print("Sharpen the gray image ...");
    unsharpedImage = cv2.addWeighted(equalizedImage, 1.5, blurredImage_gaussian, -0.5, 0);

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(uint8Image)

    # Perform fast fourier transform
    f = np.fft.fft2(equalizedImage)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    # Apply Weiner filter to reduce noise
    print("Reduce noise ...");
    filteredImage = wiener(uint8Image);

    # Apply Sobel operator for edge detection
    print("Edge detection ...");
    sobelx = cv2.Sobel(uint8Image, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(uint8Image, cv2.CV_64F, 0, 1, ksize=5)
    sobel = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0);

    # Apply thresholding for image segmentation
    print("Image segmentation ...");
    _, thresholdedImage = cv2.threshold(uint8Image, 50, 255, cv2.THRESH_BINARY);    
    # Region-based segmentation
    seed_point = (100, 100);
    segmentedImage = region_growing(uint8Image, seed_point, 20);

    # Display images in subplot
    print("Visualizing image ...");
    plt.subplot(261), plt.imshow(originalImage, cmap='gray'), plt.title('Original Image')
    plt.subplot(262), plt.imshow(equalizedImage, cmap='gray'), plt.title('Equalized Image')
    plt.subplot(263), plt.imshow(blurredImage_gaussian, cmap='gray'), plt.title('Gaussian Blurred Image')
    plt.subplot(264), plt.imshow(blurredImage_median, cmap='gray'), plt.title('Median Blurred Image')
    plt.subplot(265), plt.imshow(unsharpedImage, cmap='gray'), plt.title('Sharpened Image')
    plt.subplot(266), plt.imshow(cl1, cmap='gray'), plt.title('CLAHE Image')
    plt.subplot(267), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('Spectrum Image')
    plt.subplot(268), plt.imshow(filteredImage, cmap='gray'), plt.title('Noise-reduced Image')
    plt.subplot(269), plt.imshow(sobel, cmap='gray'), plt.title('Edge-detection Image')
    plt.subplot(2,6,10), plt.imshow(thresholdedImage, cmap='gray'), plt.title('Threshold-segmented Image')
    plt.subplot(2,6,11), plt.imshow(segmentedImage, cmap='gray'), plt.title('Region-segmented Image')
    plt.show();

    # Finished processing
    print("Finished processing.");

#Main program
def main():
    # Your main code goes here
    os.system("cls")
    testingReadingDICOMFile()
if __name__ == "__main__":
    main()