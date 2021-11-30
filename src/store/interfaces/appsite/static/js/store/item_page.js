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
    document.getElementById("added").style.visibility = "hidden";
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
        $(".q-add").innerHTML = quantity;
        setTimeout(function() {
            document.getElementById("added").style.visibility = "visible";
        }, 1000);
        document.getElementById('quantity').value  = 1;
      }
      });
    });



