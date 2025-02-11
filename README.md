## File Structure
The _csv_processing.py_ file holds the function for parsing a CSV. Its primary function is to read each CSV file.

The _api_clients.py_ file is where the API key endpoints are designated. Its primary function is to send payloads to Permutive's API.

The _main.py _file is where the program scrubs my directory for the correct CSV files, calls back to the csv_processing & api_clients file, holds the API payload, & uses multiple f-strings to make reading requests & responses easier.

## Seting up a VM in GCP
I have configured a lightweight VM in GCP to run it. Its computing power is low since this is a simple task.

### Step 1
Create a VM instance, name it something relative to the project & configure the compute power to use a cheap general-purpose system(E2). Make sure that the VM is located closest to your current location. Also, leave the default storage selection(10 GB) & Image as is.
![Create Instance](https://github.com/user-attachments/assets/4c838e7c-d022-4b89-b8bf-2cff7e4eac5f)

![Machine Config](https://github.com/user-attachments/assets/782f67da-5e3f-4442-9e40-7c02ce4255a3)

![OS   Storage](https://github.com/user-attachments/assets/fe7a6802-c50e-4c69-9dcf-4d8c0d535118)


### Step 2
Click into the Networking tab & ensure you are allowing HTTPS traffic(Note: I allowed HTTP traffic as well since this VM will be deleted in 7-10 days). Then, click over to the Observability & Security tabs. These settings can be left as is.
![Networking](https://github.com/user-attachments/assets/54303d71-b1ce-4e0b-bd58-6091e57de0f8)

![Observability(Add Cost)](https://github.com/user-attachments/assets/8660a997-fc34-4565-b34a-05343c7fd52e)

![Secruity](https://github.com/user-attachments/assets/91868a6a-b709-4fa0-9867-a484d9469ec4)

### Step 3
Using the top left side navigation/hamburger menu, click into & enable "Cloud Storage." Then, we name the storage something relevant to the project, leave its storage class as standard, configure its location to match the VM we created(I used the US - multi-region for this simple project), leave the "soft delete policy" active as the default data protection settings will be enough protection & be cost-effective.
![Cloud Storage](https://github.com/user-attachments/assets/b9870da3-48f1-4fa5-8810-a3ae10b71299)


### Step 4
Using the top left side navigation/hamburger menu, click into the Cloud Run tab & then click on "write a function" on the upper right of the screen. Here, we can name our Function something relevant to the project, configure the location/region to match what we've used in previous steps and configure the runtime to use the latest Python version since this is the language we used on our local machine.
<img width="892" alt="Cloud Run" src="https://github.com/user-attachments/assets/975b6d92-ed93-4fad-9170-72bf511e7340" />

Now, we add a trigger so that whenever data/files are added to the Cloud Storage we set up earlier, this function will run.
![Function Trigger](https://github.com/user-attachments/assets/9ce9faa9-0544-4a96-af1a-2cf7cef6e3d8)


### Step 5
Add the local/GitHub repository code to the Cloud Run main.py file to run the Function.
<img width="1278" alt="Screenshot 2025-02-11 at 10 35 58 AM" src="https://github.com/user-attachments/assets/3a14bf80-9bf5-4da2-9b5d-39b8eedb3bda" />
