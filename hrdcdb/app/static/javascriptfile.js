window.onload=function(){
//    if (document.getElementsByClassName("delBtn")){
//        // assign button to a variable
//        var delBtn = document.getElementById("delBtn")
//        
//        //add an alert when click
//        delBtn.addEventListener("click", function(){
//            alert('Are you sure you want to delete this record?')
//        })
//    }
    $(".delBtn").on( "click", function() {
        // when user tries to delet a record, make them confirm
        if (confirm("Are you sure?")){
            console.log("confirmed delete");
            var $row = jQuery(this).closest('tr');
            //var $columns = $row.find('.serviceRecordID');
            var $recordToDelete = $row.find('.serviceRecordID');
            var $clientID = jQuery(this).closest('tr').find('.clientID').text();
            console.log("clientid: " + $clientID);
            var $value = $recordToDelete.text();
            console.log($value);
            
            // send ajax get with parameters to delete
            var $urlString = 'add_Service_' + $clientID;
            console.log("url: " + $urlString)
            $.ajax({
                url: $urlString,
                type: 'GET',
                data: {'recordID': $value,},
                success: function(response) {
                    // if the response is a success, remove the table row
                    $row.remove();
                    console.log(response);
                },
                error: function(error){
                    console.log(error);
                    $.ajax({
                        url: $urlString,
                        type: 'GET'
                    });
                }
            });
                        
        } else {
            console.log("user concelled");
        }
    });

}