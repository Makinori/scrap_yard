
// database //////////
var greeted = false;  

function makeImage (path) {
    image = new Image ();
    image.src = path;
    return image;
}

var emotes={nomal:  makeImage("yome/nomal.png"),
            sangry: makeImage("yome/sangry.png"),
            smile:  makeImage("yome/smile.png")};


// base-function //////////////////

var text_area_id = "say_yome";
var image_area_id = "emote_yome";

var choice_state = [0, 1, 2, 3].map (function (num)
                                     {return {value:   "選択肢"+num,
                                              id:      "choice"+num,}});
var choicing = null;
var default_choice_values = [ "お話する", "選択肢1", "選択肢2", "黙らせる"];

function sayYome(tml_code){
    document.getElementById(text_area_id).innerHTML=tml_code;
}

function emoteYome(emotes_key){
    document.getElementById(image_area_id).src = emotes[emotes_key].src;
}

function setChoiceValue (arr){ // arg : ["c1", "c2"... "cn"]
    for (var i=0; i<choice_state.length; i++){
        if (arr[i]!=""){
            document.getElementById(choice_state[i]['id']).value = arr[i];
            choice_state[i]['value']=arr[i];
        }
    }
}

function pressChoice (choice_num) {
    choicing = choice_num;
}

function resetChoice () {
    choicing = null;
    setChoiceValue(default_choice_values);
}

// talk-data ////////////////////
function nomalYome (){
    emoteYome('nomal');
    sayYome("");
}

function silentYome () {
    sayYome("嫁は静かになった");
}

function bars (){
}

function talkYome (){
    if (!greeted){
        resetChoice()
        sayYome ("おはようさん");
        greeted=true;
    }else if (choicing == 0) {
        sayYome ("お話")
        
    }else if (choicing == 3) {
        silentYome();
    } else if (choicing!=null){
        sayYome("そのボタン"+choicing+"を押してしまったか")
        setChoiceValue(["解せぬ","解せぬ","解せぬ", "解せぬ"])
        
    }else {
        resetChoice();
        nomalYome();
    }
    choicing = null;
}


// game-loop //////////

function callYome(){
    talkYome ();
    choiceing = null;
    setTimeout("callYome()", 500);
}


callYome();
