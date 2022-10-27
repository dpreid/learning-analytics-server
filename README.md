# Learning analytics

These scripts will be run as a docker app on an AWS server for serving analytics data to student learning analytics dashboards.

Currently contains boilerplate script from Tim Drysdale's go-pocketvna repo and scripts used in the learning-analytics repo for manual generation of all user learning analytics data. These scripts will be streamlined into the script that will run on message functions and a python package containing helper functions.


## JSON command format

For receiving logging messages from a remote lab UI the format should be:

```
{user: uuid, 
t: 1234567, 
type: "log", 
exp: "spinner",
payload: payload}
```

Where ```type``` is either "log" for logging new data to a user or "request" for returning the analytics data to a user dashboard.

The payload differs, but is along the lines of:

```
{log:voltage, "data": {set: value}}
```

Where log will be equal to the state set: voltage, voltage_ramp, position, position_ramp.....