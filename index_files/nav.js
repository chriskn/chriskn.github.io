$("ul.nav a").each(function() {
    $(this).on("click", function(){
        $(".content").load($(this).attr("data-page"));
    });
});

$("div a").each(function() {
    $(this).on("click", function(){
        $(".content").load($(this).attr("bikes/data-page"));
    });
});

$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});