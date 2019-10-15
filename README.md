# Cultural_Centre
Collecting data from vk.com of a students to derive a clusterization variables

The essential files here:
1) API contains an information about the standalone VK_API application, the version of the current API and the client_id
2) groups.py collect all subscribers from target groups with open accounts
3) students.py from the programs' csv files collect all students, find their possible pages at vk.com among the subscribers of the target
groups, then verify them by the number of friends from their study program. the verified pages of the student are collected with their
subscriptions, then the vectors of their subscriptions among the most popular groups are stored into csv files for each program
