# Fermi LAT
## David Mercanti, Dhruv Jagdishkumar Patel, Alexis Richardson, Pratik Shukla
## Introduction
The Fermi Gamma-ray Space telescope has been in service since June 2009.  Observations are made by the Large Array Telescope (or LAT) which is the principal instrument attached to the Fermi Space Observatory. The LAT scans the night sky daily for photon events which indicate high energy photons coming from a recorded point in the sky, at a recorded energy. The data recorded is in fits files, and is collected weekly. Here, we try to aggregate data from multiple weeks of data, and we manage to do it automatically.   
  
  
This code will allow the user to view fit files into visualization format.

## Running the GUI
1. Make a virtual environment
    `python -m venv \path\to\new\virtual\environment`
2. start the virtual environment
        `.\path\to\new\virtual\environment\Scripts\activate`
3. download requirements
    `pip install -r requirements.txt`
4. run the GUI
    `python GUI.py`
## Running cmd
if step 1-3 has not but done, then please follow those step in GUI
1. run the cmd
    `python main.py`
      
## Few results   
 ![Occurrence-LB-week-152](https://user-images.githubusercontent.com/34422998/161398673-18739a9e-5ca2-4d9e-91e5-ab7df79a6ec9.jpg)
  
 ![Energy-LB-week-152](https://user-images.githubusercontent.com/34422998/161398693-0f5a21f5-3b11-4b3b-8d97-bb0ae9b3304a.jpg)  
 
 ![Occurrence-RADEC-weeks-009-to-010](https://user-images.githubusercontent.com/34422998/161398709-59fa1820-2a90-4e61-a060-4ebe684fa5b2.jpg)  
 
 ![Energy-RADEC-weeks-009-to-010](https://user-images.githubusercontent.com/34422998/161398747-e0dec1fa-453f-4b78-98af-d49003149fb5.jpg)
