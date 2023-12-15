$(document).ready(function(){
  $('.btn-counter').click(function(e){
      var button_classes, value = +$('.counter').val();
      button_classes = $(e.currentTarget).prop('class');        
      if(button_classes.indexOf('up_count') !== -1){
          value = (value) + 1;            
      } else {
        if(button_classes.indexOf('down_count') !== +1)
          value = (value) - 1;            
      }
      value = value < 0 ? 0 : value;
      $('.counter').val(value);
  });  
  $('.counter').click(function(){
      $(this).focus().select();
  });
});