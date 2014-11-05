$(document).ready(function() {
    location.href = '#slide1'
    $('body').bind("keydown", function(event) {
        if (event.keyCode == '40' || event.keyCode == '39' || event.keyCode == '34') {
            var x = location.href;
            var currentSlideNumber = x.split('#slide')[1];
            var nextSlideNumber = currentSlideNumber + 1;
            if (currentSlideNumber) {
                nextSlideNumber = parseInt(currentSlideNumber) + 1;
            }
            var targetAtual = "#slide" + currentSlideNumber
            $( targetAtual ).fadeOut(200);
            var target = '#slide' + nextSlideNumber;
            $("html, body").animate({
                scrollTop: $(target).offset().top,
                scrollLeft: $(target).offset().left,
            }, 200, function() {
                location.href = target;
            });
            $(target).slideDown(700);
        } else if (event.keyCode == '38' || event.keyCode == '37' || event.keyCode == '33') {
            var x = location.href;
            var currentSlideNumber = x.split('#slide')[1];
            var nextSlideNumber = parseInt(currentSlideNumber) - 1;
            var targetAtual = "#slide" + currentSlideNumber
            $( targetAtual ).fadeOut(200);
            var target = '#slide' + nextSlideNumber;
            $("html, body").animate({
                scrollTop: $(target).offset().top,
                scrollLeft: $(target).offset().left,
            }, 200, function() {
                location.href = target;
            });
            $(target).slideDown(700);
        }
        else if (event.keyCode == '27' || event.keyCode == '36') {
            var x = location.href;
            var currentSlideNumber = x.split('#slide')[1];
            var nextSlideNumber = 1;
            var target = '#slide' + nextSlideNumber;
            $("html, body").animate({
                scrollTop: $(target).offset().top,
                scrollLeft: $(target).offset().left,
            }, 200, function() {
                location.href = target;
            });
        }
    });
});

$("a[href*=#]").bind("click", function(event) {
    event.preventDefault();
    console.log('you');
    var target = $(this).attr("href");
    $("html, body").stop().animate({
        scrollTop: $(target).offset().top,
        scrollLeft: $(target).offset().left,
    }, 1500, function() {
        location.href = target;
    });
});

