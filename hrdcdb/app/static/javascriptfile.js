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
    $(document).on("click", ".addBtn", function() {
        var tr = $(this).closest('tr').clone();
        tr.find("input").attr("class", "rmBtn");
        $(".familyView").append(tr);
    });
    $(".searchBtn").on("click", function() {
        var $first_name = $("#first_name").val()
        var $middle_name = $("#middle_name").val()
        var $last_name = $("#last_name").val()
        var $dob = $("#dob").val()
        var $SSN = $("#SSN").val()
        var data = "first_name="+$first_name+"&middle_name="+$middle_name+"&last_name="+$last_name+"&dob="+$dob+"&SSN="+$SSN

        $.ajax({
                url: '/client_search',
                type: 'GET',
                data: data,
                success: function(response) {
                    $('div#response tr:gt(0)').hide();
                    $('div#response table').append(response.data);
                    console.log(response);
                },
                error: function(error){
                    console.log(error);
                                    }
            });
    });
    $(".commit").on("click", function() {
        

        var program = $(".program").val()
        // data needs to be a list of client ids
        client_ids = []
        $(".familyView .cid").each(function() {
            client_ids.push( $(this).text());
        });
        var ids = client_ids.join(',');

        var result = {"client_ids":ids,"program":program}

        $.ajax({
                url: '/create_family',
                type: 'GET',
                dataType : 'json',
                contentType: 'application/json',
                data: result,
                success: function(response) {
                    // message that says successful transaction?
                    $('table.familyView tr:gt(0)').remove();
                    alert(response.message);
                    console.log(response);
                },
                error: function(error){
                    // Useful error message
                    console.log(error);
                }
            });
    });
};
