import kombu
requested_queues = ["queue1","queue2","queue3"]
# Creating the connection
conn = kombu.Connection('amqp://user:password@10.11.12.13:5672/vhost')# or example 'amqp://guest:guest@localhost:5672/'
conn.connect()

# create a manager object
client = conn.get_manager()
# get all the queues associated with the virtual host. default vhost is "/"
queues = client.get_queues('vhost')

# print outputs
print("%30s %7s %7s %7s" % ("QUEUE" , "WORKING", "WAITING","CONSUMERS"))
for queue in queues:
    if queue.get("name") in requested_queues:
        print("%30s %7s %7s %7s" % (str(queue.get("name")) , 
        str(queue.get("messages_unacknowledged")), 
        str(queue.get("messages_ready")),
        str(queue.get("consumers"))))
