$(document).ready(function(){
    //$(".form-group label").addClass("col-sm-3 text-right")
    $(".form-group input").addClass("form-control");
    $(".form-group select").addClass("form-control");
    $(".form-group textarea").addClass("form-control").attr("rows",5);
    $(".editform input").attr("readonly","readonly")
    $("ul.errorlist").addClass("alert alert-danger")
    $(".form-group select[multiple]").css("height","200px");
    $(function () {
        $('[data-toggle="popover"]').popover()
    })
    $(".navbar-form input").addClass("input-sm");
});