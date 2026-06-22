let swiper = new Swiper(".home-slider", {
    autoplay:{
        delay:3000, 
        disableOnInteraction: false,
    },
    pagination:{
        el:".swiper-pagination",
        clickable: true,
    },
    loop: true,
});

const insVideo = document.querySelector(".ins_flex");

if(insVideo){

    Array.from(insVideo.children).forEach((item) =>{

        const duplicateNode = item.cloneNode(true);

        duplicateNode.setAttribute("aria-hidden", true);

        insVideo.appendChild(duplicateNode);

    });

}

$(document).ready(function(){
    $(window).on('scroll load', function(){
        $('#menu').removeClass('fa-times');
        $('.navbar').removeClass('active');

        if($(window).scrollTop() > 60){
            $('.header').addClass('active');
        }else{
            $('.header').removeClass('active');
        }
        $('section').each(function(){
            let top = $(window).scrollTop();
            let height = $(this).height();
            let offset = $(this).scrollTop().top;
            let id = $(this).attr('id');

            if(top >= offset && top < offset + height){
                $('.navbar a').removeClass('active');
                $('.navbar').find('[href="#${id}"]'.addClass('active'));
            }
        });
    });
});

//menu mudança de cor
let menu = document.querySelector('#menu');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    navbar.classList.toggle('active');
};

// SCROLL HEADER
window.onscroll = () => {
    let header = document.querySelector('.header');

    if (window.scrollY > 50) {
        header.classList.add('ativo');
    } else {
        header.classList.remove('ativo');
    }
};