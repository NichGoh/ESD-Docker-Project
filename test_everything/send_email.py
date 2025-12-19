from flask import Flask, request, jsonify
from flask_mailman import Mail, EmailMessage
# from flask_cors import CORS
import amqp_connection
import json
import pika
# import os, sys


queue_name = "reservation_confirmation"

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'testing.for.flaskmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'isbp lowv qilm enda' #Testing123!
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

temptitle = ""
tempmessage = ""
receiver = 'testing.for.flaskmail@gmail.com'

def receiveLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print('activity_log: Consuming from queue:', queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"activity_log: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("activity_log: Program interrupted by user.") 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nactivity_log: Received an order log by " + __file__)
    processLog(json.loads(body))
    print()

def processLog(log):

    userid = log["user_id"]
    receiver = log['email']
    # receiver = "nicholasgoh.2022@scis.smu.edu.sg"


    rest_name = log["restaurant_name"]
    # rest_name = "placeholder"
    res_id = log['reservation_id']
    res_date = log['reservation_date']
    num_pax = log['num_of_pax']
    title = "Reservation booked #" + str(res_id)
    message = "Hello " + userid +",\nYour reservation for " + rest_name + " on " + res_date + " for " + str(num_pax) + " has been booked!"

    with app.app_context():
        msg = EmailMessage(title, message, 'testing.for.flaskmail@gmail.com', [receiver])
        msg.send()
    return "Email sent!"

if __name__ == '__main__':
    print("send_email: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("Email: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)