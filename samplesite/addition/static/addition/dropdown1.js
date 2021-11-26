$('.dropdown1').click(function () {
    $(this).toggleClass("active")
    $(this).find('.dropdown-menu').slideToggle(300);
});

$('.dropdown1').focusout(function () {
    $(this).toggleClass("active")
    $(this).find('.dropdown-menu').slideUp(300);
});

$('.dropdown1 .dropdown-menu li').click(function () {
    $(this).parents('.dropdown').find('span').text($(this).text());
    $(this).parents('.dropdown').find('input').attr('value', $(this).attr('id'));
});
