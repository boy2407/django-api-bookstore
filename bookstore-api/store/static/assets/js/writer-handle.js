$( document ).ready(function() {
  //Link đến trang mua sách
  $("#featured-courses").flickity({
    wrapAround: true,
    pageDots: false,
    initialIndex: 1,
    accessibility: true, //true by default
    autoPlay: false, // advance cells every 3 seconds
    groupCells: 2
  });
  
  function goDoSomething(identifier) {
    alert("data-id:" + $(identifier).data('paragraph'));
  }
  
  //Tip: it is better not to use margin-right and margin-left to add spaces between each slide as the Flickity slide position could be inperfect, giving an undesirable result. Instead, use padding or add the margin to the child element to make up the space between the slide.
  
  jQuery(document).ready(function($) {
  
    $('.lightbox_trigger').click(function(e) {
  
      //prevent default action (hyperlink)
      e.preventDefault();
  
      //Get clicked link href
      var image_href = $(this).attr("href");
  
      /* 	
      If the lightbox window HTML already exists in document, 
      change the img src to to match the href of whatever link was clicked
      
      If the lightbox window HTML doesn't exists, create it and insert it.
      (This will only happen the first time around)
      */
  
      if ($('#lightbox').length > 0) { // #lightbox exists
        var article = document.getElementById('lightbox_trigger');
        //place href as img src value
        $('#content').html( '<iframe width="480" height="277" src="' + article.dataset.embed + '" /> ' + '<p> ' + article.dataset.paragraph + '</p>' );
       
  
        //show lightbox window - you could use .show('fast') for a transition
        $('#lightbox').fadeIn();
      } else { //#lightbox does not exist - create and insert (runs 1st time only)
        var article = document.getElementById('lightbox_trigger');
  
        //create HTML markup for lightbox window
        var lightbox =
          '<div id="lightbox">' +
          '<p>Click to close</p>' +
          '<div id="content">' + //insert clicked link's href into img src
          '<iframe width="480" height="277" src="' + article.dataset.embed + '" /> ' +
          '<p> ' + article.dataset.paragraph + '</p>' +
          '</div>' +
          '</div>';
  
        //insert lightbox HTML into page
        $('body').append(lightbox);
      }
  
    });
  
    //Click anywhere on the page to get rid of lightbox window
    $(document).on('click', '#lightbox', function() { //must use live, as the lightbox element is inserted into the DOM
      $('#lightbox').fadeOut();
    });
  
  });

});