// Load all content before rendering #body div content

$(window).ready(function() {
    $('#body').show();
    $('#loading').hide();
});


// Quantity Buttons

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


// Delete entry cross

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


// Stripe checkout

fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});