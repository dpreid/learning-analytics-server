# Learning analytics client

![Learning Analytics logo](./img/learning_analytics_icon.png)

This project provides a set of scripts for adding graph based learning analytics (LA) to the practable.io remote labs. The scripts utilise the same relay [INSERT LINK to relay script] used to communicate with individual remote lab experiments, but uses a separate websocket connection (in addition to data and video websockets) for two way communication using JSON strings between these analytics scripts running on a server and the analytics dashboard that users interact with [INSERT LINK to dashboard repo]. 

LA is used in this context to provide formative feedback to student users of remote labs. Details of the design and an evaluation of the system will be available in a future publication.

![LA UI Upper](./img/LA_UI_upper.png)
![LA UI Lower](./img/LA_UI_lower.png)



## Setup

A detailed example of how to setup the analytics server is given in [SETUP README](./setup/README.md).

A basic overview of setting up on AWS server.

### 1) Create and setup AWS server

t2.medium is the recommended minimum.

### 2) systemd service files

A systemd service file for each remote lab experiment needs to be generated (on your local machine) that sets the logging URL, data and comparison graph directory environment variables and starts a separate client script for each remote lab instance. These can then be moved to the appropriate location on the server.

### 3) run session-rules

This requires access to the necessary secrets provided by your administrator and they should be available on your local machine at ```~/secret/sessionrelay.pat``` for example.

A session-rules script needs to be created for the custom set of remote lab hardware you wish to connect to. See example in [example session-rules script](./setup/files/session-rules)


## JSON command format

For receiving logging messages from a remote lab UI the format should be:

```
{user: uuid, 
t: 1234567, 
type: "log", 
exp: "spinner",
payload: payload}
```

Where ```type``` is either "log" (which will be ignored by the analytics client); "analytics" for processing new data to a user; or "request" for returning the analytics data to a user dashboard.

The payload differs, but is along the lines of:

```
{log:voltage, "data": {set: value}}
```

Where log will be equal to the state set: voltage, voltage_ramp, position, position_ramp.....


## Running on Amazon AWS EC2 instance

Currently using a t2.medium server with 30Gb of storage. Each Python process only requires ~1% of CPU even when logging at high frequency (every 50ms).

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




## Background logging

In previous runs of remote labs we used a different script that was manually run daily to capture data.

Logging websockets are attached to remote hardware that stream along with video and data. The ```log-script``` folder contains the scripts necessary for running the background logging.
The ```connect.sh``` script outputs the stream for a single piece of hardware for a set duration using, for example:

```
./connect.sh spin30 log 20

```

This would stream log data from spin30 to an output in log/ for 20 seconds.

## Automated logging

To automate the daily task of running background logging, attempts were made to run it on crontab -e but there were issues when attempting to run on AWS server, so resorted to manually starting the scripts daily.

## Logging location

AWS server was used to log all data, which was then manually downloaded to local machine for analysis.

To backup this, will also have a Raspberry Pi doing the same logging.