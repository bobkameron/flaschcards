from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.db.models import Model

from django.views.decorators.csrf import csrf_exempt

from .models import Card 
import json 

import datetime 

# Create your views here.



def index(request):
    return render ( request, "cards/index.html")

def get_current_datetime():
    # returns current datetime in utc timezone
    return datetime.datetime.now(tz = datetime.timezone.utc )


def next_card(request):
    '''
    Specification 

    Input: request- HTTP get request

    Output: Returns an HTTP JSON response with the next card to be shown, if there is any. 
    
    Else, returns an HTTP JSON error response status 404 with key 'error' detailing the error 
    '''

    if request.method != "GET":
        return JsonResponse({"error": "Wrong request method- use HTTP GET to request next card"} ,status = 400)

    current_datetime = get_current_datetime() 

    # Select all cards that are not in bin 11, and user has gotten wrong less than 10 times 
    binned_cards = Card.objects.exclude(bin = 11).exclude(number_times_incorrect__gte = Card.max_incorrect)

    print(binned_cards, Card.objects.all())

    if len(binned_cards) == 0:
        # No more cards to review 
        return JsonResponse({"error": "You have no more words to review; you are permanently done!"} ,status = 404)
    else:
        # Select cards that are not in bin 0/11, that have non-positive timer and gotten wrong less than 10 times
        binned_cards_bin_nonzero = binned_cards.exclude(bin = 0).exclude(datetime_to_next_appearance__gt = current_datetime).order_by('-bin','datetime_to_next_appearance')
        
        card = None 

        if len(binned_cards_bin_nonzero) > 0:
            card = binned_cards_bin_nonzero[0]
        else:
            binned_cards_bin_zero = Card.objects.filter(bin = 0).order_by ('datetime_to_next_appearance')

            # if there are cards in bin zero, we need to return a card from this bin. 
            if len(binned_cards_bin_zero) > 0:
                card = binned_cards_bin_zero[0]

        if card is not None:
            return JsonResponse( { 'card_id' :card.id , 'card_word' : card.word, 'card_definition': card.definition, 'card_bin':card.bin  }, status = 200)
        else:
            return JsonResponse({"error": "You are temporarily done; please come back later to review more words."} ,status = 404)



@csrf_exempt 
def guess_card(request, card_id):
    '''
    Specification:

    Input: request: must be an HTTP JSON PUT request that has key - value pair  guess: boolean indicating
    if the user guessed the crad correctly or not. 

    card_id = must be a valid id of a flash card in our database. 

    Output: 
    HTTP JSON response with status code 204 if the card's status of being guessed correctly or incorrectly
    was successfully updated. 

    '''
 
    # return JsonResponse({"test time_delta": Card.time_delta } , status = 200)

    # Check if right request method
    if request.method != "PUT":
        return JsonResponse({"error": "Wrong request method- use HTTP PUT to guess card right or wrong"} ,status = 400)

    data = json.loads(request.body)

    # Check if request body's JSON string is in right format 
    if 'guess' not in data or type(data['guess']) != bool :
        return JsonResponse({"error": "Request body must be in JSON format with key-value pair 'guess':boolean included"} ,status = 400)

    guess_right = data ['guess']

    try:
        card = Card.objects.get(id = card_id )
        
        if card.bin == Card.highest_bin or card.number_times_incorrect == Card.max_incorrect:
            return JsonResponse({"error": "Cannot guess on a card that you have gotten wrong 10 times or is in bin 11"} ,status = 400)

        if guess_right:
            # if we guess right just increment the bin.
            new_bin = min ( card.bin + 1 , Card.highest_bin )  

            # Json response message
            message = "Successfully guessed the card" 
        else:
            # if we guess wrong make the bin go to 1 and then incrrement number of incorrect 
            new_bin = 1  
            card.number_times_incorrect = min(card.number_times_incorrect + 1, Card.max_incorrect)

            message = "Guessed wrong on the card"

        card.bin = new_bin 
        if new_bin < Card.highest_bin:
            card.datetime_to_next_appearance = get_current_datetime() + Card.time_delta[new_bin]

        card.save()  


        return JsonResponse({"status": message} ,status = 200)

    except Model.DoesNotExist:
        return JsonResponse({"error": "No card matching card_id exists in our database "} ,status = 400)

    # We should never get here 
    assert False