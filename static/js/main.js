$(document).ready(function(){
    $("#blog").submit(function(e){
        e.preventDefault();
        blog();
    });

    $(document).on('click', '.delete2', function() {
        delete_blog($(this).closest("tr").attr("id"));
    });

    $(".entry").each(function() {
        var option = {trigger : $(this).find(".edit2"), action : "click"};
        var id = $(this).attr("id");
        $(this).find(".editable").editable(option, function(e){
            edit_blog(id, e.value);
        });
    });

$(function () {
    $(document).on("change", ":file", function() {
            var id = $(this).closest('tr').attr('id');
               if (this.files && this.files[0]) {
                var reader = new FileReader();
                var file = this.files[0];
                var formData = new FormData();
                formData.append("id", id);
                formData.append("filename", file.name);
                formData.append("data", file);
                reader.onload = function(e) {
                    $('#myImg' + id).attr('src', e.target.result); 
                    var request = new XMLHttpRequest();
                    request.open("POST", "/upload");
                    request.send(formData);
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});


    function blog(){
        $.ajax({
            type: 'POST',
            url: "/blog",
            data: {
                "text": $("#Post").val()
            },
            dataType: 'json',
            success: function(response, status) {
                var thing = $("#Post").val();
                var id = response["id"];
                var html = "<tr id=" + id + " class=\"entry\">" +
                "<td><img id=\"myImg"+ id +"\"src=\"uploads/background.jpg\" alt=\"your image\" align=\"bottom\" width=500px height=400px/>" +
                "<span class =\"editable\">" + thing + "</span>\n" +
                "<span class=\"created_at\">Created At: "  + "</span>" +
                "<span class=\"updated_at\">Updated At: " + "</span>" +
                "<input type=\"button\" value=\"delete\" class=\"delete2\"/>\n" + 
                "<input type=\"button\" value=\"edit\" class=\"edit2\"/>" +
                "<label class=\"file_button\">" +
                "<input type=\'file\'/>chooseFile</label>" +
                 "</td></tr>";
                $("#posts tr:first").after(html);
                var option = {trigger : $("#" + id).find(".edit2"), action : "click"};
                $("#" + id).find(".editable").editable(option, function(e){
                    edit_blog(id, e.value);
                });

                var update = response['updated_at'];
                var formated_update = moment(update).add(7, 'hours').format('YYYY-MM-DD HH:mm:ss');
                $("#" + id).find(".updated_at").html("Updated At: " + formated_update);

                var create = response['created_at'];
                var formated_create = moment(create).add(7, 'hours').format('YYYY-MM-DD HH:mm:ss');
                $("#" + id).find(".created_at").html("Created At: " + formated_create);
            }
        });
    };

    function delete_blog(id) {
        $.ajax({
            type: 'DELETE',
            url: "/blog/" + id, 
            data: {},
            dataType: 'json',
            success: function(response, status) {
                $("#" + id).remove()
            }
        });
    };


    function edit_blog(id, updated_text) {
        $.ajax({
            type: 'PUT',
            url: "/blog/" + id, 
            data: {
                "text": updated_text
            },
            dataType: 'json',
            success: function(response, status) {
                var update = response['updated_at'];
                var formated_update = moment(update).add(7, 'hours').format('YYYY-MM-DD HH:mm:ss');
                $("#" + id).find(".updated_at").html("Updated At: " + formated_update);
            }
        });

 

    };