```
 ____                              ____                _ _             
/ ___|  ___ _ __  ___  ___  _ __  |  _ \ ___  __ _  __| (_)_ __   __ _ 
\___ \ / _ \ '_ \/ __|/ _ \| '__| | |_) / _ \/ _` |/ _` | | '_ \ / _` |
 ___) |  __/ | | \__ \ (_) | |    |  _ <  __/ (_| | (_| | | | | | (_| |
|____/ \___|_| |_|___/\___/|_|    |_| \_\___|\__,_|\__,_|_|_| |_|\__, |
                                                                 |___/
TIMER TRIGGER                                                      
```

# SENSOR READING TIMER TRIGGER FUNCTION

This is an Azure Timer Trigger function that runs every hour, gets temperature and moisture values from a sensor interface and saves them in an Azure Table.

To develop this function, it was used Microsoft Azure Storage Explorer with Azurite, and a simple Node.js server to simulate response from sensor. 

---
### Tools
Install:  
[Azure Data Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer/#Download-4)  
[Azurite](https://learn.microsoft.com/pt-br/azure/storage/common/storage-use-azurite?tabs=visual-studio-code%2Cblob-storage#install-azurite)

With Python (3.11.9)
```
python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
```

---
### Execution
- Start Azurite in VSCode by clicking these buttons:  
![image](https://github.com/user-attachments/assets/d229a9a3-f3bc-4ec7-a5d1-b0abb860e4e0)

- Open Microsoft Azure Storage Explorer, click 'Emulator & Attached' and create your own resources  
![image](https://github.com/user-attachments/assets/bb819b4c-de82-45b5-ab36-80543a771cf9)

- Run function
`func start`

---
### Table records example
![image](https://github.com/user-attachments/assets/6ad41c74-567c-46e2-852f-ea26b546754c)

---
![LOGO](https://github.com/user-attachments/assets/33897bc4-2f12-4d5e-a81b-e0294a48eada)  

Developed by: Bruno Polli
