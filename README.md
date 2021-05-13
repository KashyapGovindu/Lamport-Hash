# Lamport-Hash
Implementation of Leslie Lamport One-Time Password scheme using Python, sqlite3 and SHA-256 algorithm for hashing

## Contents
**Basic** Directory  
**server.py** - Lamport implementation on server side(Bob) without salt  
**client.py** - Lamport implementation on client side(Alice) without salt
<br>
<br>
**Enhanced** Directory  
**enhancedServer.py** - Lamport implementation on server side(Bob) without salt  
**enhancedClient.py** - Lamport implementation on client side(Alice) without salt 
<br>
<br>
**Common files in both implementations**  
**lamport.py** - All functions regarding Lamport scheme implementation for both salt and basic versions  
**sql_db.py** - All functions regarding SQL implementation for server side database using sqlite3 

## Python Libraries/Modules Used
- socket
- sys
- _thread
- threading
- hashlib - *SHA-256 implementation is mentioned here* 
- sqlite3
 
## Requirements
1. **sqlite3** should be installed in the system
2. **Python3** (>=3.8) should be installed in the system
3. (Optional) Install DB Browser for sqLite to view databases  
   
## Commands
1. CLone this repo into your local system/ Download the zip file
> **For Basic Lamport Hash**
 1. Go to `Basic` directory
 2. Run `./server.py` first
 3. In another terminal, run `./client.py`
 4. Enter the inputs as messages in program provide

> **For Enhanced Lamport Hash**
1. Go to directory where all the files above are present
2. Run `./enhancedServer.py` first
3. In another terminal, run `./enhancedClient.py`
4. Enter the inputs as messages in program provide

**NOTE:** In both cases, Username should be unique for each client due to implementation constraints
