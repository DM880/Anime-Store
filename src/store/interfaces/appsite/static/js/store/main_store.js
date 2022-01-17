// Added to cart div

function addedCart(item_id) {
  if (document.getElementById("added"+item_id) != null) {
    setTimeout(function() {
      document.getElementById('added'+item_id).style.opacity = 1;
      document.getElementById('added'+item_id).classList.remove("display-none-added");
    },);
    setTimeout(function(){
      document.getElementById('added'+item_id).style.opacity = 0;
      document.getElementById('added'+item_id).classList.add("display-none-added");
    }, 2000);
  }
}

// Add items to cart without refreshing page

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