#Libraries
import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt

#Testing function
def testingReadingDICOMFile():
    #Initializing
    print("Initializing...")

    #Reading dicom file
    print("Reading dicom file...")
    dicomFilePath = "../../Data/CAD_Data/dicom_lung"
    dicomFile = [pydicom.dcmread(os.path.join(dicomFilePath, f)) for f in os.listdir(dicomFilePath) if f.endswith('.dcm')]

    #Print the number of files loaded
    print(f"Loaded {len(dicomFile)} DICOM files")

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