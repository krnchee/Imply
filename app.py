from flask import Flask, request, jsonify
import math
import random

app = Flask(__name__)

global participants
participants = []

# Post route for issunig new raffle tickets to someone
@app.route('/issue_tickets', methods = ['Post'])
def issue_tickets():
    name = request.args.get('username')
    new_tix = request.args.get('number_of_tickets')

    try:
        new_tix = int(new_tix)
    except ValueError:
        return 'Please enter a positive integer value of starting tickets'

    if not new_tix or new_tix < 0:
        return 'Please enter a positive integer value of starting tickets'

    if len(name) == 0:
        return 'Please enter a username!'

    new_part = True

    if len(participants) > 0:
        for part in participants:
            if part['name'] == name:
                new_part = False
                part['tickets'] += new_tix
                total_tix = part['tickets']
                return "We have added {} tickets to the raffle. "\
                "{} you now have {} total tickets in the raffle!".format(new_tix, name, total_tix)

    if new_part:
        participant = {}
        participant['name'] = name
        participant['tickets'] = new_tix
        participants.append(participant)

    return 'We have placed your {} tickets in the raffle {}. Good luck!'.format(new_tix, name)

# Post route for transfering raffle tickets
@app.route('/transfer_tickets', methods = ['Post'])
def transfer_tickets():
    donor = request.args.get('donor')
    recipient = request.args.get('recipient')
    transfer_tix = request.args.get('number_of_tickets')

    try:
        transfer_tix = int(transfer_tix)
    except ValueError:
        return 'Please enter a positive integer value of number of tickets to transfer'

    if not transfer_tix or transfer_tix < 0:
        return 'Please enter a positive integer value of starting tickets'

    if len(donor) == 0 or len(recipient) == 0:
        return 'Please enter both a donor and recipient!'

    if len(participants) < 1:
        return 'The Donor is not registered in this raffle.' \
                'Please register first!'

    found_donor = False
    new_part = True

    for part in participants:
        if part['name'] == donor:
            found_donor = True
            donor_tix = part['tickets']
            if donor_tix < transfer_tix:
                return "{} only has {} tickets to their name! Please adjust number of tickets to transfer."\
                .format(donor, donor_tix)
            part['tickets'] -= transfer_tix
            donor_tix = part['tickets']

    if not found_donor:
        return 'We could not find {} in our system. Please enter a donor name that is registered.'

    for part in participants:
        if part['name'] == recipient:
            new_part = False
            part['tickets'] += transfer_tix
            recipient_tix = part['tickets']
            return "We have successfully transfered {} tickets! "\
            "{} now has {} total tickets and {} now has {} total tickets!"\
            .format(transfer_tix, donor, donor_tix, recipient, recipient_tix)

    if new_part:
        participant = {}
        participant['name'] = recipient
        participant['tickets'] = transfer_tix
        participants.append(participant)

    return "We have successfully transferred {} tickets! "\
    "{} now has {} total tickets and new participant {} now has {} total tickets!"\
    .format(transfer_tix, donor, donor_tix, recipient, transfer_tix)

# Get route that returns one winner from the raffle
@app.route('/select_winner', methods = ['GET'])
def select_winner():
    weighted_participants = []

    if len(participants) < 1:
        return 'No participants have entered this raffle yet.' \
                'Register now to win!'

    for part in participants:
        weighted_participants += [part['name']] * part['tickets']

    winner = random.choice(weighted_participants)

    for part in participants:
        if part['name'] == winner:
            part['tickets'] -= 1
            if part['tickets'] == 0:
                participants.remove(part)


    return 'The winner is {}! Congrats!'.format(winner)

# Get route that returns list of all participants
@app.route('/list_of_participants', methods = ['GET'])
def list_of_participants():

    if len(participants) < 1:
        return 'No participants have entered this raffle yet.' \
               'Register now to win!'

    part_list = 'Here are a list of all participants:\n'

    for part in participants:
         part_list += part['name'] +'\n'

    return part_list


if __name__ == "__main__":
    app.run(debug=True)
