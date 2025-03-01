# Analytics Setup

Below are detailed setup instructions for use of this analytics code on a remote server (or SBC like Raspberry Pi as a backup). The example provided is for setting up with a specific set of equipment (spin30-41) therefore amendments will be required for different hardware.

## Setting up the session host

All commands are run on the host (e.g. AWS server) unless otherwise stated. The assumption is that you are running Ubuntu 20.04 (or above) on both host and local machines. Generation of autogenerated directory with access tokens will be on your local machine that is pre-setup with the necessary secrets.

### 1. Install golang

```
$ cd ~/sources/go
$ wget https://go.dev/dl/go1.19.5.linux-amd64.tar.gz
$ which go #check if already installed
$ sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.5.linux-amd64.tar.gz #if a version is installed, remove it, and then install
$ cp /etc/profile ~/etc.profile.old #safety copy!
$ sudo /etc/profile #add line at end: export PATH=$PATH:/usr/local/go/bin
$ diff ~/etc/profile.old /etc/profile #check change is ok
$ source /etc/profile #make change take effect in current session (this might remove syntax highlighting)
$ echo $PATH #check path updated 
$ rm ~/etc.profile.old #we don't need this anymore (assuming you are confident previous edits were ok)
$ go version #verify installation successful
go version go1.19.5 linux/amd64
```

### 2. Install relay

```
$ cd ~/sources
$ git clone https://github.com/practable/relay.git
$ cd relay
$ go mod tidy
$ cd cmd/session
$ go build
$ sudo cp session /usr/local/bin/session-relay
$ which session 
/usr/local/bin/session
```

### 3. Create files

#### File structure

Using nano (or otherwise), copy and paste the contents below into new files, named and located as identified below:

#### session.service (to go in `/etc/systemd/system`)

```
[Unit]
Description=session host streaming service
After=network.target
[Service]
Restart=on-failure
ExecStart=/usr/local/bin/session-relay host

[Install]
WantedBy=multi-user.target session-rules.service
```

#### session-rules.service (to go in `/etc/systemd/system`)
```
[Unit]
Description=apply session host streaming rules
After=network.target session.service
Wants=session.service
PartOf=session.service

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 10
ExecStart=/usr/local/bin/session-rules

[Install]
WantedBy=multi-user.target
```

#### session-rules (to go in /usr/local/bin)
An example script is provided in [./files/session-rules](./files/session-rules). Below is an example for setting up session-rules for spin30-spin41

```
#!/bin/sh
spin30AccessFile="/etc/practable/log.access.spin30"
spin31AccessFile="/etc/practable/log.access.spin31"
spin32AccessFile="/etc/practable/log.access.spin32"
spin33AccessFile="/etc/practable/log.access.spin33"
spin34AccessFile="/etc/practable/log.access.spin34"
spin35AccessFile="/etc/practable/log.access.spin35"
spin36AccessFile="/etc/practable/log.access.spin36"
spin37AccessFile="/etc/practable/log.access.spin37"
spin38AccessFile="/etc/practable/log.access.spin38"
spin39AccessFile="/etc/practable/log.access.spin39"
spin40AccessFile="/etc/practable/log.access.spin40"
spin41AccessFile="/etc/practable/log.access.spin41"

spin30TokenFile="/etc/practable/log.token.spin30"
spin31TokenFile="/etc/practable/log.token.spin31"
spin32TokenFile="/etc/practable/log.token.spin32"
spin33TokenFile="/etc/practable/log.token.spin33"
spin34TokenFile="/etc/practable/log.token.spin34"
spin35TokenFile="/etc/practable/log.token.spin35"
spin36TokenFile="/etc/practable/log.token.spin36"
spin37TokenFile="/etc/practable/log.token.spin37"
spin38TokenFile="/etc/practable/log.token.spin38"
spin39TokenFile="/etc/practable/log.token.spin39"
spin40TokenFile="/etc/practable/log.token.spin40"
spin41TokenFile="/etc/practable/log.token.spin41"

spin30Access=$(cat "$spin30AccessFile")
spin31Access=$(cat "$spin31AccessFile")
spin32Access=$(cat "$spin32AccessFile")
spin33Access=$(cat "$spin33AccessFile")
spin34Access=$(cat "$spin34AccessFile")
spin35Access=$(cat "$spin35AccessFile")
spin36Access=$(cat "$spin36AccessFile")
spin37Access=$(cat "$spin37AccessFile")
spin38Access=$(cat "$spin38AccessFile")
spin39Access=$(cat "$spin39AccessFile")
spin40Access=$(cat "$spin40AccessFile")
spin41Access=$(cat "$spin41AccessFile")

spin30Token=$(cat "$spin30TokenFile")
spin31Token=$(cat "$spin31TokenFile")
spin32Token=$(cat "$spin32TokenFile")
spin33Token=$(cat "$spin33TokenFile")
spin34Token=$(cat "$spin34TokenFile")
spin35Token=$(cat "$spin35TokenFile")
spin36Token=$(cat "$spin36TokenFile")
spin37Token=$(cat "$spin37TokenFile")
spin38Token=$(cat "$spin38TokenFile")
spin39Token=$(cat "$spin39TokenFile")
spin40Token=$(cat "$spin40TokenFile")
spin41Token=$(cat "$spin41TokenFile")


curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin30","destination":"'"${spin30Access}"'","id":"0","token":"'"${spin30Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin31","destination":"'"${spin31Access}"'","id":"1","token":"'"${spin31Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin32","destination":"'"${spin32Access}"'","id":"2","token":"'"${spin32Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin33","destination":"'"${spin33Access}"'","id":"3","token":"'"${spin33Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin34","destination":"'"${spin34Access}"'","id":"4","token":"'"${spin34Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin35","destination":"'"${spin35Access}"'","id":"5","token":"'"${spin35Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin36","destination":"'"${spin36Access}"'","id":"6","token":"'"${spin36Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin37","destination":"'"${spin37Access}"'","id":"7","token":"'"${spin37Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin38","destination":"'"${spin38Access}"'","id":"8","token":"'"${spin38Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin39","destination":"'"${spin39Access}"'","id":"9","token":"'"${spin39Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin40","destination":"'"${spin40Access}"'","id":"10","token":"'"${spin40Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin41","destination":"'"${spin41Access}"'","id":"11","token":"'"${spin41Token}"'"}' http://localhost:8888/api/destinations
```

### 4. Run service scripts 

#### Procedure for systemd setup of session

```
sudo su
cd /etc/systemd/system
nano session.service        #copy in contents above
systemctl enable session
systemctl start session

```

#### Procedure for systemd setup of session-rules

```
nano /usr/local/bin/session-rules       #copy in above contents
chmod +x /usr/local/bin/session-rules   #make executable
```

#### Generate tokens we need 

Generating tokens is performed on your local machine (where you need to have access to the appropriate secrets).

Use the `configure` script in `scripts/` as follows - these are modified from [spinner-amax](https://github.com/practable/spinner-amax) to only generate access files and tokens for the logging streams.

```
./configure spin 30 41 https://relay-access.practable.io
```

#### Copy the files to the server 

On your local machine:
```
cd ../autogenerated
tar -cvf session-files.tar ./*
scp -i ~/your-key.pem user@server:~
```

On the server:

```
#server
mkdir -p /etc/practable
mv /home/ubuntu/session-files.tar /etc/practable
cd /etc/practable
tar -xvf session-files.tar
rm session-files.tar
```

#### Enable service

```
nano session-rules.service #copy in contents above
systemctl enable session-rules
systemctl start session-rules
```

#### Check that the rules are looking ok

```
# on the analytics server
curl -X GET http://localhost:8888/api/destinations/all
```

You should see destinations for all of the spinners you added in the rules file (not copied in here because they contain credentials)

Now you can connect your logging applications to the local streams, which are:

```
ws://localhost:8888/ws/spin30
ws://localhost:8888/ws/spin31
ws://localhost:8888/ws/spin32
ws://localhost:8888/ws/spin33
ws://localhost:8888/ws/spin34
ws://localhost:8888/ws/spin35
ws://localhost:8888/ws/spin36
ws://localhost:8888/ws/spin37
ws://localhost:8888/ws/spin38
ws://localhost:8888/ws/spin39
ws://localhost:8888/ws/spin40
ws://localhost:8888/ws/spin41
```

You can try connecting using websocat, e.g. 

```
websocat ws://localhost:8888/ws/spin30 - --text
```

### 5. Run (python) analytics client for each piece of hardware

The recommendation is to use a dedicated server that will only be running python with these analytics scripts and therefore a virtual environment is not necessary. Since we then don't have any issues with other services needing python, we are free to configure the system python3 to have the packages we need for this client script.

#### Add scripts to correct locations

Ensure that the following scripts are all in `/opt/analytics/` on the server:

```
client.py
analytics.py
process.py
response.py
TaskDistance.py
```

As well as the comparison graphs in `/opt/analytics/comparison_graphs/`

Create a data directory at `/var/analytics/data/`. This is where student data will be stored.

#### Add necessary packages

We also need to add the python packages whilst root (this could cause system issues so don't do this on a shared server)

```
sudo su
pip3 install websocket-client
pip3 install networkx
pip3 install pyvis
pip3 install matplotlib

```

#### Copy logging instance service files

We use `scripts/sessionservice` to make one copy of this file for each logging instance (and this is done when you call the `configure` script earlier)
```
[Unit]
Description=session host streaming service
After=network.target session.service session-rules.service
[Service]
Environment="LOG_URL=ws://localhost:8888/ws/spin30"
Restart=on-failure
ExecStart=/usr/bin/python3 /opt/analytics/client.py

[Install]
WantedBy=multi-user.target 
```

Copy each hardware service file above into /etc/systemd/system on the server and add the enable and disable shell scripts to the home folder to allow quick enabling and disabling of all logging services.

#### Start analytics clients

Run the `./enable-logging-clients.sh` script to start the service for each of the logging instances.


# Additional information

## Write/Read speed

move to parquet/feather and cvontinue to work with pandas due to [speedup](https://towardsdatascience.com/optimize-python-performance-with-better-data-storage-d119b43dd25a)


## Adding another public key

1. [get public key from private key info](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/describe-keys.html#retrieving-the-public-key)

```
ssh-keygen -y -f /path_to_key_pair/my-key-pair.pem
```

2. Log into server using amazon dashboard (or directly if have existing auithorized pem on hand)

```
nano .ssh/authorized_keys ##add public key on new line
```

Add a space and the name of the public key e.g.

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClKsfkNkuSevGj3eYhCe53pcjqP3maAhDFcvBS7O6V
hz2ItxCih+PnDSUaw+WNQn/mZphTk/a/gU8jEzoOWbkM4yxyb/wB96xbiFveSFJuOp/d6RJhJOI0iBXr
lsLnBItntckiJ7FbtxJMXLvvwJryDUilBMTjYtwB+QhYXUMOzce5Pjz5/i8SeJtjnV3iAoG/cQk+0FzZ
qaeJAAHco+CY/5WrUBkrHmFJr6HcXkvJdWPkYQS3xqC0+FmUZofz221CBt5IMucxXPkX4rWi+z7wB3Rb
BQoQzd8v7yeb7OzlPnWOyN0qFU0XA246RA8QFYiCNYwI3f05p6KLxEXAMPLE example-key
```