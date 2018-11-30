$(document).ready(function () {
    buttonPress();

    // AJAX pagination
    $('body').on('click', '.paginator-arrow', function(event) {
        event.preventDefault();
        var url = ($(this)[0].href);
        if ($(this)[0].id == 'prev'){
          myState.pop()
          myState.pop()
        }
        ajax_get_update(url);
    });

    // highlight related events
     $('body').on('mouseover', '.card.family', function() {
          // check if there is 2 or more related events on a page
          if ($(".card.family").length >= 2){
              $(".card.family").addClass("highlighted-family");
          }else{ // if there is only one family event on a page, add regular highlighting
              $(".card.family").addClass("highlighted");
          }
     });

    $('body').on('mouseout', '.card.family', function() {
            $(".card.family").removeClass("highlighted-family");
            $(".card.family").removeClass("highlighted");
    });
});

// scroll to top
function scroll_to_top(){
  $('html, body').animate({ scrollTop: 0 }, 'slow');
}

// pagination related
function ajax_get_update(url)
    {
    //get the parts of the result you want to update. Just select the needed parts of the response
    $.ajax({
        async: true,
        type: "GET",
        url: url,
        cache: true,
        success: function(result){
              sessionStorage.setItem("result", result);
              update_content(result);
              update_history(url);
            }
    });
}

function update_content(result) {
    var events = $("#events", result);
    var paginator = $("span.step-links", result);
    $('#events').replaceWith(events);
    $('.step-links').replaceWith(paginator);

    // scroll to the top on a new page
    scroll_to_top();

}


let myState = [];
function update_history(url) {
  // window.history is only updated when the current url is not
  // saved in our private history
  if (!myState.includes(url)) {
    history.pushState(url, url, url);
    myState.push(url);
  }
}

window.addEventListener('popstate', function(event){
    result = sessionStorage.getItem("result");
    update_content(result);
    location.reload();
    event.stopPropagation()
    scroll_to_top();

});
// end of pagination related staff


// search bar animation
$(document).on('click', ".promgruz-search", function(event){
    // scroll to the top
    scroll_to_top();

    // unfold white background
    if ($('.search-background.anim-search').length===0) {
        $('.search-background').addClass('anim-search').removeClass('anim-search-rev')}
    else {
        $('.search-background').removeClass('anim-search').addClass('anim-search-rev')
    }

    // reveal the search bar
    if ($('.top_content.anim-search-bar').length===0) {
        $('.top_content').addClass('anim-search-bar').removeClass('anim-search-bar-rev')}
    else {
        $('.top_content').removeClass('anim-search-bar').addClass('anim-search-bar-rev')
    }
    event.stopPropagation()
});

$('.promgruz-search').onclick = function(){}

// close search bar
$(document).on('click', ".icon_close", function(){
    $('.search-background').removeClass('anim-search').addClass('anim-search-rev');
    $('.top_content').removeClass('anim-search-bar').addClass('anim-search-bar-rev');
});

// hamburger animation
$(document).on('click', "button.navbar-toggler", function(event){
    if ($('.promgruz-navbar.anim').length===0) {
        $('.promgruz-navbar').addClass('anim').removeClass('animrev')}
    else {
        $('.promgruz-navbar').removeClass('anim').addClass('animrev')
    }
    event.stopPropagation()
});


function buttonPress() {
    var myURL=window.location.pathname;
    if(myURL == "/"){
        $('#upcoming').addClass('menu-active')
    }else{
        $('#past').addClass('menu-active')
    }
}
