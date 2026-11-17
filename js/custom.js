$(function () {
  if ($(".realized__gallery").length) {
    $(".realized__gallery").each(function () {
      var $gallery = $(this);

      var $dots = $gallery.find(".realized__dots");
      var gap = 6;

      $gallery.on("touchstart mousedown", function (event) {
        event.stopPropagation();
      });

      var sizeBars = function (swiper) {
        var count = swiper.slides.length || 1;
        var available = $gallery.innerWidth();
        var width = Math.min(62, (available - gap * (count - 1)) / count);

        $dots.css("--bar", width + "px");
      };

      new Swiper(this, {
        nested: true,
        speed: 400,
        navigation: {
          prevEl: $gallery.find(".realized__prev")[0],
          nextEl: $gallery.find(".realized__next")[0],
        },
        pagination: {
          el: $dots[0],
          clickable: true,
        },
        on: {
          init: sizeBars,
          resize: sizeBars,
        },
      });
    });

    var $realized = $(".realized");

    new Swiper(".realized__slider", {
      slidesPerView: 3,
      spaceBetween: 16,
      speed: 400,
      watchOverflow: true,
      nested: true,
      navigation: {
        prevEl: $realized.find(".examples__prev")[0],
        nextEl: $realized.find(".examples__next")[0],
      },
      pagination: {
        el: $realized.find(".examples__dots")[0],
        clickable: true,
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 2,
        },
        1024: {
          slidesPerView: 3,
        },
      },
    });
  }

  if ($(".examples__slider").length) {
    var $examples = $(".examples");

    new Swiper(".examples__slider", {
      slidesPerView: 4,
      spaceBetween: 16,
      speed: 400,
      watchOverflow: true,
      navigation: {
        prevEl: $examples.find(".examples__prev")[0],
        nextEl: $examples.find(".examples__next")[0],
      },
      pagination: {
        el: $examples.find(".examples__dots")[0],
        clickable: true,
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
          spaceBetween: 12,
        },
        768: {
          slidesPerView: 2,
          spaceBetween: 16,
        },
        1024: {
          slidesPerView: 4,
          spaceBetween: 16,
        },
      },
    });
  }
});
