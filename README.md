# WifitrackProject
The data set "Campus_Analytics_Hashed_201805-201806.json" we used contains sensitive information, therefore we cannot publish it.

Install packages:

`pip3 install flask`
`pip3 install multiprocessing`
`pip3 install numpy`
`pip3 install pickle`

API used:
Googlemap API, Highchart API

Preprocess:

`split -l 100000 Campus_Analytics_Hashed_201805-201806.json splitdata`

`python3 preprocessOneHourOneFile.py`


Start the server:

`python3 __init__.py`
