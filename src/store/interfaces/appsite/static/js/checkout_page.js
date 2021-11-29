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