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

        }

        function declineContactRequest(button){
            console.log('decline' + ' ' + button.val());
        }
    </script>