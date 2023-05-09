# Analytics Setup

# Setting up AWS EC2 or Raspberry Pi for running analytics client

Setup instructions for background logging servers (including on Raspberry Pi for backup). The examples provided are for setting up with a specific range of equipment (spin30-41) therefore amendments will be required for different hardware.


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

## Setting up the session host

### install golang

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

### clone repo

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

Now let's get some files from the [spinner-amax](https://github.com/practable/spinner-amax) repo, that we use for setting up session host on the experiments as systemd services.

We need:

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
This is the version for a spinner, with two streams (the logging streams are not connected to the hardware). We will modify this to have streams for each spinner's logging stream, since we are only interested in collecting analytics from the logging streams and not the video and data streams.
```
#!/bin/sh
videoTokenFile="/etc/practable/video.token"
videoAccessFile="/etc/practable/video.access"
dataTokenFile="/etc/practable/data.token"
dataAccessFile="/etc/practable/data.access"

videoToken=$(cat "$videoTokenFile")
videoAccess=$(cat "$videoAccessFile")
dataToken=$(cat "$dataTokenFile")
dataAccess=$(cat "$dataAccessFile")

curl -X POST -H "Content-Type: application/json" -d '{"stream":"video","destination":"'"${videoAccess}"'","id":"0","token":"'"${videoToken}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"data","destination":"'"${dataAccess}"'","id":"1","token":"'"${dataToken}"'"}' http://localhost:8888/api/destinations 
```



### Procedure for systemd setup of session

```
sudo su
cd /etc/systemd/system
nano session.service #copy in contents above
systemctl enable session
systemctl start session

```

### Producedure for systemd setup of session-rules

#### Write session-rules script 

We need a connection for every spinner in the range spin30-spin41
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

```
nano /usr/local/bin/session-rules #copy in above contents
chmod +x /usr/local/bin/session-rules #make executable
```

#### Generate tokens we need 

Use the `configure` script in `scripts/` as follows (these are modified from [spinner-amax](https://github.com/practable/spinner-amax) to only generate access files and tokens for the logging streams.

```
./configure spin 30 41 https://relay-access.practable.io
```

copy the files to the server ...

```
cd ../autogenerated
tar -cvf session-files.tar ./*
scp -i ~/your-key.pem user@server:~
```

```
#on the server
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

You can try connecting using websocat, e.g. 


websocat ws://localhost:8888/ws/spin30 - --text

### Python client

We could use Docker, but initial testing is indicating that network modes need sorting out, and since we don't have any issues with other services needing python, we are free to configure the system python3 to have the packages we need for this client script.

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

Copy each hardware service file above into /etc/systemd/system on the server/RPi and add the enable and disable shell scripts to the home folder to allow quick enabling and disabling of all logging services.


We also need to add the python packages whilst root (this could cause system issues so don't do this on a shared server)

```
sudo su
pip3 install websocket-client
pip3 install networkx
pip3 install pyvis
pip3 install matplotlib

```


The python code is using 5-26% CPU on t2.medium with no logging taking place (17% shown in image below, but varies every few seconds)

```

ubuntu@ip-172-31-32-44:~$ top


top - 15:16:47 up 3 min,  1 user,  load average: 11.64, 5.63, 2.21
Tasks: 131 total,  13 running, 118 sleeping,   0 stopped,   0 zombie
%Cpu(s): 88.8 us, 11.2 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   3921.0 total,   2657.4 free,    662.0 used,    601.6 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   3036.5 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND                                                                                
   2753 root      20   0  183696  78292  27112 R  17.3   1.9   0:00.57 python3                                                                                
   2757 root      20   0  178216  72412  25840 R  17.3   1.8   0:00.54 python3                                                                                
   2743 root      20   0       0      0      0 R  17.0   0.0   0:00.75 python3                                                                                
   2747 root      20   0  186384  81788  27940 R  17.0   2.0   0:00.66 python3                                                                                
   2750 root      20   0  184904  79772  27472 R  16.3   2.0   0:00.60 python3                                                                                
   2749 root      20   0  184904  79804  27504 R  16.0   2.0   0:00.59 python3                                                                                
   2754 root      20   0  179968  74044  25856 R  16.0   1.8   0:00.55 python3                                                                                
   2762 root      20   0  166928  64316  23880 R  14.7   1.6   0:00.44 python3                                                                                
   2770 root      20   0  137456  41552  19992 R   7.0   1.0   0:00.21 python3                                                                                
   2772 root      20   0  136432  41020  20092 R   7.0   1.0   0:00.21 python3                                                                                
      1 root      20   0  101996  11276   8268 S   0.7   0.3   0:06.25 systemd                                                                                
   2777 root      20   0   16268   9700   5992 R   0.7   0.2   0:00.02 python3                                                                                
     22 root      20   0       0      0      0 S   0.3   0.0   0:00.29 ksoftirqd/1                                                                            
    174 root      19  -1   59772  22016  20836 S   0.3   0.5   0:01.39 systemd-journal                                                                        
    466 root      20   0  242896  11264   8316 S   0.3   0.3   0:00.18 accounts-daemon                                                                        
    499 root      20   0   16620   7524   6648 S   0.3   0.2   0:00.16 systemd-logind                                                                         
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kthreadd                                                                               
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_gp                                                                                 
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_par_gp                                                                             
      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 slub_flushwq                                                                           
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 netns                                                                                  
      7 root      20   0       0      0      0 I   0.0   0.0   0:00.00 kworker/0:0-cgroup_destroy                                                             
      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/0:0H-kblockd                                                                   
      9 root      20   0       0      0      0 I   0.0   0.0   0:00.14 kworker/u30:0-events_unbound                                                           
     10 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_percpu_wq                                                                           
     11 root      20   0       0      0      0 S   0.0   0.0   0:00.00 rcu_tasks_rude_                                                                        
     12 root      20   0       0      0      0 S   0.0   0.0   0:00.00 rcu_tasks_trace                                                                        
     13 root      20   0       0      0      0 R   0.0   0.0   0:00.26 ksoftirqd/0       

```

This load was found to be the scripts erroring out due to mnissinbg libraries. There is about 22% load on start up now, but soon disappear without traffic.

## File organisation

Must avoid multiple processes writing to the same files - could cause messages to be garbled or processes to pause pending on file being available (more of a windows thing) but gnerally, it's a code smell to have race conditions like this.

So proposal - write to `user-hardware.log` so that there is only a single process writing to any given file.

When it is time to provide analytics, the users' files will have to be located and read (directory walk using glob pattern)

You won't get the message rate you need with open/close on each file (benchmarked elsewhere at 300ms/line)


## Write/Read speed

move to parquet/feather and cvontinue to work with pandas due to [speedup](https://towardsdatascience.com/optimize-python-performance-with-better-data-storage-d119b43dd25a)


## multiple websocket clients

use async approach, with dispatcher:

https://websocket-client.readthedocs.io/en/latest/examples.html#dispatching-multiple-websocketapps
note that rel is not availabe on conda, so need to use pip install and skip running in spyder 



Asyncio has more complicated syntax that golang, but it gets the job done (eventually)/ [This example](https://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio) looks fairly complete (and models what you would do to set up a periodic dump of the adjacency matrix to file)

```python
import asyncio

async def periodic():
    while True:
        print('periodic')
        await asyncio.sleep(1)

def stop():
    task.cancel()

loop = asyncio.get_event_loop()
loop.call_later(5, stop)
task = loop.create_task(periodic())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
```

Note you should also add in keyboard interrupt so that you can Ctrl-C your script to stop, and/or stop it from systemctl.


## Global store

It's not elegant to have global variables, but this is probably the quickest way to get the job done. Just need to add a mutex!
Everyone operation that touches the store object needs to request the lock first, then release when done.
Since you are using asyncio, then using their lock would be a good start: https://docs.python.org/3/library/asyncio-sync.html
Usual traps are hanging when lock is not released, or when a subroutine requests a lock that has already been requested and obtained by the calling routine.
