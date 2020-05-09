# Imply-HW

This app allows a user to enter a unique username and a number of tickets to participate
in a raffle. There is also functionality to transfer tickets from an existing participant,
to another participant (either an existing participant or a new one).

Once there is a participant, the app allows the ability to select a winner.
The winner is selected randomly from all the tickets registered.
The winning ticket is removed from the raffle and from there a new winner can
be selected, until there are no more tickets available to select.

##Instructions

Need Python installed!

First create virtual environment by running source venv/bin/activate

Next run pip install -r requirements.txt

Start app by running python app.py

##REST APIs:

To retrieve all participants:

GET request on localhost:5000/list_of_participants:

ex) http://localhost:5000/list_of_participants

To select a winner:

GET request on localhost:5000/select_winner:

http://localhost:5000/select_winner

To add ticket to a new/existing participant:

POST request on localhost:5000/issue_tickets:

username - must be unique for each participant
number_of_tickets - must be a positive integer

ex) http://localhost:5000/issue_tickets?username=adam&number_of_tickets=500

To transfer tickets from an existing participant to another participant:

POST request on localhost:5000/transfer_tickets:

donor - must be an existing participant, prior to this call
recipient - new or existing participant
number_of_tickets - number of tickets to be transferred from donor to
                    recipient. Donor must have the number of tickets to be transferred

ex) http://localhost:5000/transfer_tickets?donor=john&recipient=jam&number_of_tickets=100


##Analysis

All apis have an O(n) time and space complexity, where n is the number of participants.
This is due to scanning the array which holds all the participants.
The only api which has a worse complexity is the select_winner api. It is also O(n) for
space and time, however n in this case is number of tickets, which can be much larger then
the number of participants.

There are several ways to optimize this. One is to create a global array of weighted winners
and modify it, instead of building a new one every time the select_winner api is called.
Another way is to not use an array at all for the weighted list of participants and
doing so would have the select_winner api have the same time and space complexity as
the rest of the apis. I did not attempt this, because I was informed that completeness is
valued more then optimization, so I wanted to finish the app.
