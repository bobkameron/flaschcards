

document.addEventListener('DOMContentLoaded', function() {
    show_next_card();
} );



function hide_main() {
    let main_body = document.querySelector("#main");
    main_body.style.display = 'none';
}

// ( { 'card_id' :card.id , 'card_word' : card.word, 'card_definition': card.definition, 'card_bin':card.bin  }, status = 200)


function show_main() {
    let main_body = document.querySelector("#main");
    main_body.style.display = 'block';
}

function get_card_front () {
    return document.querySelector("#card_front");
}

function get_card_back() {
    return document.querySelector ("#card_back_side");
}

function get_card_message () {
    return document.querySelector ('#no_card_message'); 
}

function show_front_card () {
    get_card_div().style.display = 'block';
    get_card_front().style.display = 'block';
    get_card_back().style.display = 'none';
    get_card_message().style.display = 'none';
    show_main();
}

function get_card_correct () {
    return document.querySelector("#get_card_correct");
}

function get_card_wrong () {
    return document.querySelector("#get_card_wrong");
}

function guess_card (guess ) {
    // guess is a boolean here, either true or false based on if user guessed correctly or not 

    hide_main(); 

    let json_body = JSON.stringify ( {'guess': guess });
    
    let card_id = get_card_div().dataset.card_id; 

    fetch ( `/card/${card_id}`  , { method: "PUT" , body : json_body})
    .then ( result => {
            if (!result.ok) throw result;
            console.log(result);
            return result.json(); 
        }  )
    .then(   
        result => {
            show_next_card(); 
        }
    )
    .catch( error => {
        console.log(error);
        show_next_card();
    }
    )
}


function show_back_card() {

    /*
    let card_wrong = get_card_wrong(); 
    let card_correct = get_card_correct();
    
    card_wrong.addEventListener( 'click' , guess_card (false));

    card_correct.addEventListener('click' , guess_card (true));
    */

    get_card_div().style.display = 'block';
    get_card_front().style.display = 'none';
    get_card_back().style.display = 'block';
    get_card_message().style.display = 'none';

    show_main();
}

function get_card_div () {
    return document.querySelector("#card"); 
}

function get_card_word () {
    return document.querySelector ( "#card_word");
}

function get_card_definition (){
    return document.querySelector( "#card_definition");
}

function get_show_definition_div() {
    return document.querySelector ( "#show_definition" );
}


function show_no_card_message (message) {
    message_div = get_card_message();
    message_div.innerHTML = message; 

    get_card_div().style.display = 'none';
    message_div.style.display = 'block';
    show_main();
}

function show_next_card() {

    hide_main(); 

    fetch("/card/next" ,  {method: "GET" }  )
    .then( result => {
        if (!result.ok) throw result;
        console.log(result);
        return result.json(); } 
    )
    .then(
    result => {
        console.log(result, result['card_word'])

        get_card_word().innerHTML = result['card_word'] ;
        get_card_definition().innerHTML = result['card_definition'];

        let card_div = get_card_div();
        card_div.dataset.card_id = result['card_id'];

        card_div.dataset.card_bin = result['card_bin'];
        
        let show_definition = get_show_definition_div(); 

        show_definition.addEventListener('click', function () {
            show_back_card(); 
        }  )

        let card_wrong = get_card_wrong(); 
        let card_correct = get_card_correct();
        
        card_wrong.addEventListener( 'click' , function () {
             guess_card (false)}
             );
    
        card_correct.addEventListener('click' , function () {
            guess_card (true)
        });


        show_front_card();

    }
    )
    .catch( error => {
        hide_main(); 
        console.log(error);
        error.json().then (
            result => {
                console.log( result , result['error']);
                
                show_no_card_message (result['error']);
            }
        );
    }
    )
    


}






