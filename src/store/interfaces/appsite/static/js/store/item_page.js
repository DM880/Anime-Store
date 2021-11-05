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


document.getElementById("nav").style.border = 'none';