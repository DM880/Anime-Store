function decrementValue(item_id)
{
    var id = item_id
    var value = parseInt(document.getElementById('quantity'+id).value);
    if(value > 1){
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById('quantity'+id).value = value;
    }
}


function incrementValue(item_id)
{
    var id = item_id
    var value = parseInt(document.getElementById('quantity'+id).value);
    if(value < 10){
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('quantity'+id).value = value;
    }
}


var a = $('.delete-itm');
a.on('click', function(e){
  e.preventDefault();
    var entry_id = $(this).attr('data-id')
    var url = $('#delete-entry'+entry_id).attr('href');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      // Ajax Call
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json',
        success: function(data){
            window.location.href = data.url;
        }
      });
    });
