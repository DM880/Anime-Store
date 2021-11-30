function decrementValue()
{
    var value = parseInt(document.getElementById('quantity').value);
    if(value > 1){
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById('quantity').value = value;
    }
}


function incrementValue()
{
    var value = parseInt(document.getElementById('quantity').value);
    if(value < 10){
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('quantity').value = value;
    }
}


var btn = $('.add');
btn.on('click', function(e){
  e.preventDefault();
    var quantity = parseInt(document.getElementById('quantity').value);
    var url = $('#form').attr('action');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
      // Ajax Call
      $.ajax({
        type: 'POST',
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        data:  {"quantity":quantity},
        dataType: 'json',
        success: function(response){
          document.getElementById('quantity').value  = 1;
        }
      });
    });



