
# FoETools
Some tools you can use to manage your villages. Mostly written in Python 3

## [FlatDeposits](FlatDeposits.py)

#### Usage
1. Use your browser's Developer Tool to get the heaviest JSON response (For me ~60KB. Higher era may generate heavier data) named 'json?h=*session id*' and paste it in a file located in the same folder as this script.
2. Save the file as "data.json"
3. Run it!

#### Execution
Linux
```bash
  $ python3 FlatDeposits.py
```
Windows
```batch
  C:\> py -3 FlatDeposits.py
```
## [GetMotivators](GetMotivators.py)

#### Prerequisites
In order to use this script you have to install ["pyperclip"](https://pypi.org/project/pyperclip/). A Python's library that helps you get the content of the clipboard (CTRL+C's content)

##### Install pyperclip
Linux
```bash
  $ sudo pip3 install pyperclip
```
Windows, open CMD as administrator
```batch
  C:\Windows\System32> py -3 -m pip install pyperclip
```
#### Execution
Linux
```bash
  $ python3 GetMotivators.py
```
Windows
```batch
  C:\> py -3 GetMotivators.py
```
And let it running...

#### Usage
1. Open your browser's Developer Tool to get every JSON response
2. Open FoE and click on the Town Hall -> News -> Event History
3. Click on the menu tab and enable filter options
4. Filter only "Social Interactions" events
5. Now, copy every JSON response from your admin panel (Right click -> Copy -> Copy response)

#### Results
You'll see how many times every player helped you
