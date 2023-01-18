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


## Running on Amazon AWS EC2 instance

Currently using a t2.medium server with 30Gb of storage - still need to test.

Relay is used to setup the appropriate logging websockets. Each piece of hardware logging is started by systemd.

The analytics scripts are located in /opt/analytics/ on the AWS server. 
The comparison graph folder is therefore in /opt/analytics/comparison_graphs
Data should be saved to /var/analytics/data

Need to set the following environment variables:

LOG_URL for connecting to the logging websocket - defaults to localhost "ws://127.0.0.1:8000"
DATA_PATH for providing the absolute path the the directory storing user logs - defaults to "./test/data"
COMP_PATH for providing the absolute path to the comparison graphs folder - defaults to "./comparison_graphs"

Cannot use relative paths for accessing folders (such as the comparison graph folder) - so need to include the above file paths in the scripts

To get running I set HTTP, HTTPS, SSH (for logging in to EC2 instance locally) and All TCP were set in the inbound security settings. Will need to check the security of all this and exactly what is necessary. Connection through the websocket was not allowed until I set All TCP.
