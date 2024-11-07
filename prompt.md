Hello! Congratulations on making it to this round of Cribl’s interview process! The objective of
this take home exercise is to demonstrate your design and implementation techniques for a
real-world type of development problem. You can use any programming language or tech stack
of your choice. However, please note that we are looking for solutions that demonstrate your
unique code, so please limit external dependencies to a bare minimum (eg. frameworks, HTTP
servers)

ou should develop and submit code to Cribl via a github project. Please commit and push
code changes as you normally would - your thinking and working style is an important part for
us to understand.

Of course, no great product is complete without clear documentation and testing. As part of
your solution, please provide any design, usage, and testing documentation that you feel would
be helpful to someone using your solution for the first time.

Problem statement:
A customer has asked you for a way to provide on-demand monitoring of various unix-based
servers without having to log into each individual machine and opening up the log files found in
/var/log. The customer has asked for the ability to issue a REST request to a machine in order
to retrieve logs from /var/log on the machine receiving the REST request.

Acceptance criteria:
1. HTTP REST API should be the primary interface to make data requests
2. The results returned must be presented with the newest log events first.
3. The REST API should support additional query parameters which include
   a. The ability to specify a filename within /var/log
   b. The ability to specify the last n number of log entries to retrieve within the log
   c. The ability to filter results based on basic text/keyword matches
4. Must not use any pre-built log aggregation systems - this must be custom, purpose-built
   software.
5. Minimize the number of external dependencies in the business logic code path
   (framework things like HTTP servers, etc are okay)
   

Bonus points:
   There is potential to double the deal size with this customer if you can successfully implement
   “nice-to-have” features that will make your produce more valuable to them:
1. The ability to issue a REST request to one “primary” server in order to retrieve logs from
   a list of “secondary” servers. There aren’t any hard requirements for the protocol used
   between the primary and secondary servers.
2. A basic UI to demo the API