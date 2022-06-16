# Monitoring-Challenge

This is a SRE challenge received as a part of initial screening for the interview process.


### Choices made

Well I have chosen Python  as a tool for development for couple of reasons
1. Easy to develop the code
2. Got inbuilt libraries such as numpy and pandas for data analysis.
3. The installation packages are Widely available on most of the linux distribution.

### Assumptions:

1. CPX offers an API for fetching all running servers. 

2. The same service also allows you to query a given IP for simple statistics.


To Execute cpx_server.py , execute next statement

./cpx_server.py <port­ to ­serve ­on>

This simple Python server cpx_server has below two endpoints:

A) 
$curl localhost:<port>/servers
["10.58.1.121","10.58.1.120","10.58.1.123","10.58.1.122",...]

B)  
$curl localhost:<port>/10.58.1.121
{"cpu":"61%","service":"UserService","memory":"4%"}

### Trade off

Added serviceName parameter as an optional parameter in main method
  
Also, used try catch block to capture keyboardCInterrupted event.  

### Future development

- beatification of output
- work on optional parameter

### Steps to run the programs. 

1) Pre-requisite libraries 
    To download all required pre requisite, execute below commands 
  
    pip3 install pandas
    pip3 install numpy
    how to run the program

2) excute following steps to run the program

    first execute ./cpx_server.py <port­ to ­serve ­on> 
    then use same port number while triggering service_monitor.py program.
  
    ./service_monitor.py 9000 4 TicketService
  
 The various available metrics and runtime parameter while in this program 
  
  1) This is call to CPX API for fetching all running microservices.
  
  for example ./service_monitor.py 9000 1 TicketService

   2) This is call to CPX API for fetching all running microservices.
  
  for example ./service_monitor.py 9000 1 TicketService
