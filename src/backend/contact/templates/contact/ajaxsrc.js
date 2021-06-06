<script>
    function acceptContactRequest(button) {
        console.log('accept' + ' ' + button.val());

        var decision = 'accept';
        var sender_id = button.val();

        $.ajax({
            method: "POST",
            url: "{% url 'my_requests' %}",
            dataType: "json",
            async: false,
            data: { decision: decision,  sender_id: sender_id, csrfmiddlewaretoken: '{{ csrf_token }}' },
            success: function(data) {
                console.log(data.answer);
            }
        });

        $.ajax({
                method: "POST",
                url: "/contact/check_is_friend/" + person_id,
                dataType: "json",
                async: false,
                data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
                success: function(data) {
                    console.log(data.is_friend);
                }
            });

    }

    function del() {
        document.getElementById("button_popup").style.display = "none";
    }

    function acceptRequest(person_id) {
        console.log("acceptRequest is working!");

        document.getElementById("request_from_person_" + person_id).style.display = "none"

        $.ajax({
            method: "POST",
            url: "/contact/accept_request_from_user/" + person_id,
            dataType: "json",
            async: false,
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function(data) {
                console.log("User accepts the request from person_"+ person_id + ": " + data.success);
            }
        });
    }

    function declineRequest(person_id) {
        console.log("declineRequest is working!");

        document.getElementById("request_from_person_" + person_id).style.display = "none"

        $.ajax({
            method: "POST",
            url: "/contact/decline_request_from_user/" + person_id,
            dataType: "json",
            async: false,
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function(data) {
                console.log("User declines the request from person_"+ person_id + ": " + data.success);
            }
        });
    }

    function deleteContact(button_delete) {
        person_id = button_delete.value;
        console.log("deleteContact is working! person_id= " + person_id);

        document.getElementById("person_" + person_id).style.display = "none";

        // скрываем блоки с информацией о пользователе
        var profile = document.getElementsByClassName("this-user-info");
        profile[0].style.display = "none";

        // показываем подпись о выборе контакта
        var info = document.getElementsByClassName("block_info_choose");
        info[0].style.display = "block";

        $.ajax({
            method: "POST",
            url: "/contact/delete_request_from_user/" + person_id,
            dataType: "json",
            async: false,
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function(data) {
                console.log("User declines the request from person_"+ person_id + ": " + data.success);
            }
        });
    }

    function defineRelationship(person_id) {
        var statusRelationship = -1;
        $.ajax({
            method: "POST",
            url: "/contact/define_relationship_with_user/" + person_id,
            dataType: "json",
            async: false,
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function(data) {
                statusRelationship = data.relationship;
            }
        });
    }

    function createContact(person_id) {
        $.ajax({
            method: "POST",
            url: "/contact/create_contact_with_user/" + person_id,
            dataType: "json",
            async: false,
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            success: function(data) {
                console.log(data.success);
            }
        });
    }



    // onclick="document.location='{% url 'chat' %}'"
</script>
