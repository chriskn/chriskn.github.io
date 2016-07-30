$(document).ready(function() {
        $(".content").load("home.html");
});


$("ul.nav a").each(function() {
    $(this).on("click", function(){
        $(".content").load($(this).attr("data-page"));
    });
});

$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});