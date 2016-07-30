        $(".bike").each(function() {
            $(this).on("click", function(){
                $(".content").load($(this).attr("data-page"));
            });
        });