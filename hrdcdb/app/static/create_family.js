$(document).ready(function(){

$(".addBtn").on( "click", function() {
        var $row = jQuery(this).closest('tr');
        var $recordToAdd = $row.find('.clientID').text();
        console.log("clientid: " + $recordToAdd);

        $.ajax({
        	cache: false,
            url: '/create_family',
            type: 'GET',
            data: {'clientID': $recordToAdd,},
            success: function(response) {
                $(".familyView tr:last").append('<tr>something</tr>')
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        })
    })
}