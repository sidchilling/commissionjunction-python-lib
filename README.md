commissionjunction-python-lib
=============================

This is a python script to retrieve from Commission Junction the amount of commission a publisher has collected
over a period of time broken down by the advertiser ids.

A publisher will need to sign up for developer access on CJ to get a developer key which will be used in the 
script. You can signup here: https://api.cj.com/sign_up.cj

To retrieve the commission from each advertiser within a specific time period, you can use this script. An example
is shown below -

```
end_date = datetime.utcnow()
start_date = datetime.utcnow()
key = 'YOUR-DEVELOPER-KEY'
cj = CJ(key = key, end_date = end_date, start_date)
data = cj.retrieve()
```

The `data` obtained above will be of the form -

```
{'10505442': 14.0, '10796189': 10.199999999999999, '10694956': 7.0, '10965070': 12.030000000000001, 
'10938449': 2.48, '10885795': 4.29, '11129226': 1.1699999999999999}
```

This is a key-value dict with the key being the advertiser id and value is the commission from that advertiser.

Following packages are required for this script [pretty standard requirements] -

1. logging
2. BeautifulSoup
3. requests
4. datetime
5. dateutil

There are some more test cases at the end of the file `cj.py` which you should have a look at before using it.

[Please feel free to open bugs]
