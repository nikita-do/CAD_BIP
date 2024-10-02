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
    dicomFilePath = "../../Data/CAD_Data/dicom_lung/000004.dcm"
    dicomFile = pydicom.dcmread(dicomFilePath)

    #Iterate through all data elements and print their names and keywords
    for elem in dicomFile:
        print(f"Name: {elem.name}. Keyword: {elem.keyword}")

    #Access metadata
    print(f"Acquisition date: {dicomFile.AcquisitionDate}, {dicomFile.AcquisitionTime}")
    print(f"Patient name: {dicomFile.PatientName}")
    print(f"Patient age: {dicomFile.PatientAge}")
    print(f"Patient sex: {dicomFile.PatientSex}")
    print(f"Patient InstanceNumber: {dicomFile.InstanceNumber}")
    print(f"Patient SliceLocation: {dicomFile.SliceLocation}")

    #Display image
    pixel_array = dicomFile.pixel_array
    plt.imshow(pixel_array, cmap='Blues')
    plt.show()

#Main program
def main():
    # Your main code goes here
    os.system("cls")
    testingReadingDICOMFile()
if __name__ == "__main__":
    main()