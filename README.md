Flashcards App Specification 

To login to the admin page, here is the login info: 

    admin info:

        username:
        admin

        password:
        adminadmin

        email:
        eakevinjin@gmail.com


Specification of the Website:

Front-End API (returns HTML pages):

    / GET 

        For any get request to this route, this simply returns an HTML webpage which is a single page flashcard application. 

    /admin GET

        For any GET reqeust to this route, you can login to the web app using the above administrator info. Here, you can create flashcards, and view them as well. 

Back-End API (simply returns HTTP responses where the body are JSON objects):

    /card/next  GET

        For any GET request to this route, this returns JSON data about the next card that is to be shown, or else a message indicating there are no cards or some other message. 
        If there is another card to be shown, HTTP JSON status code 200 will be returned, and the method body will
        be a JSON string of format { 'card_id' : next_card_id , 'card_word' : next_card_word, 'card_definition': next_card_definition, 'card_bin': next_card_bin  }.

        If there is not another card to be shown, then an HTTP response of status code 404 where the method body 
        is a JSON string of format { 'error' : error_message}. 


    /card/id(integer) PUT

        Input: 
        The PUT request to this route must have the HTTP Body be a JSON string in the format {'guess': bool}, indicating whether or not the user guessed the card with card_id right or wrong. 

        Output:
        Returns an HTTP response where the body is a JSON string, and the status code is 200 if the user updated the
        bin on a valid card that could be updated. 
