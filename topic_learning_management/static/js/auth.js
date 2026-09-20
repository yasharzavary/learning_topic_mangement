document.addEventListener(
    "DOMContentLoaded",
    function(){

        const passwordInput =
        document.querySelector(
            "input[name='password']"
        );


        if(passwordInput){

            passwordInput.addEventListener(
                "keypress",
                function(event){

                    if(event.key === "Enter"){

                        this.closest("form").submit();

                    }

                }
            );

        }


    }
);