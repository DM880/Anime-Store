
function addedCart(item_id) {
  if (document.getElementById("added"+item_id) != null) {
    setTimeout(function() {
      document.getElementById('added'+item_id).style.visibility = 'visible';
    }, 500);
    setTimeout(function(){
      document.getElementById('added'+item_id).style.visibility = 'hidden';
    }, 2000);
  }
}



var btn = $('.add');
btn.on('click', function(e){
  e.preventDefault();
    item_id = $(this).attr('data-id');
    var url = $('#form-item'+item_id).attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      // Ajax Call
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json',
        success: function(response){
          addedCart(item_id);
        }
      });
    });