
# FoETools
Some tools you can use to manage your villages. Mostly written in Python 3

## [FlatDeposits](FlatDeposits.py)

#### Usage
1. Use your browser's Developer Tool to get the heaviest JSON response (For me ~60KB. Higher era may generate heavier data) named 'json?h=*session id*' and paste it in a file located in the same folder of [FlatDeposits](FlatDeposits.py).
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

#### Usage
1. Open your browser's Developer Tool and select the Network tab to get every FoE's server response
2. Open FoE and click on the Town Hall -> News -> Event History
3. Click on the menu button (top-left) and enable filter options (if you haven't)
4. Filter only "Social Interactions" events
5. In the Developer Tool -> Network, click on any response and click on "Save all as HAR with content"
6. Save the file in the same folder of [GetMotivators](GetMotivators.py)
7. Run it!

#### Execution
Linux
```bash
  $ python3 GetMotivators.py
```
Windows
```batch
  C:\> py -3 GetMotivators.py
```

#### Results
You'll see how many times every player helped you
