API implementation Microsatellite Engineering Project 
=================================
Microsatellite Engineering - II.1 Battery design project

## What does it do
The program uses [digikey-api](https://github.com/peeter123/digikey-api) and [py3dbp](https://github.com/enzoruiz/3dbinpacking) to request data from digi-key's database, filter it according to parameter input and optimal fitting. 
The program writes the filtered capacitors into a .txt and .csv file:
![a](https://i.imgur.com/BPIUdrx.png)

## Installation
0. _(When switched to other client_id and client_secret, remove 'token_storage.json' in '~\GitHub\Batterydesign-repo\tmp' directory.)_
1. Install all relevant packages (others should be installed by default):
   ```
   pip install digikey-api
   pip install py3dbp
   ```
2. Create a developer account [here](https://developer.digikey.com/); 
3. Under 'Organizations' create a production app, for a ['Product Information'](https://developer.digikey.com/products/product-information) API
   * Create an organization ;
   * Add a 'Production App' and set 'OAuth Callback' to ``` https://localhost:8139/digikey_callback ``` ;
   * Select 'Product Information' and save ;
   * Click on the project name and copy the clent_id and secret_id.
4. Specify the client_id, client_secret and a storage path (this is where the token_storage.json will be stored each session) --- all as a string --- as seen here:

```
import os
import re
import csv
import time
import digikey
import math as m
from digikey.v3.productinformation import KeywordSearchRequest
from py3dbp import Packer, Bin, Item 

### Battery Parameters ###
H_box = 42                      #[mm]
W_box = 34                      #[mm]
L_box = 34                      #[mm]
V_box = H_box * W_box * L_box   #[mm3]
Ah = 600e-3                     #[Ah]
V = 3.7                         #[V]
s = 3600                        #[sec]
E = Ah*V*s                      #[J]

os.environ['DIGIKEY_CLIENT_ID'] = 'client id here'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'client secret here'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = '~\\GitHub\\Batterydesign-repo\\tmp'
```

After specifiying the client_id, client_secret and storage path correctly, and running Main.py, a browswer window should pop up, click on **Advanced...** and **Accept the Risk and Continue**. This is the ``` https://localhost:8139/digikey_callback ``` that you will only see after each fresh installation of a new api product. After continuing you should see a windows as follows: 

![a](https://i.imgur.com/phhkTWr.png)

You can close the window afterwards, the auth code should now be in your ~\tmp folder.


Please refer to [digikey-api](https://github.com/peeter123/digikey-api) and [py3dbp](https://github.com/enzoruiz/3dbinpacking) for additional details regarding the digikey api for python and py3dbp package.

## How does it work
![](https://github.com/casruks/Batterydesign-repo/blob/main/FlowDiagramAPI.png)
