jQuery(function($) {
  var $body = $('body');
  var $menu = $('#sidedrawer');

  function showMenu() {
    var options = {
      onclose: function() {
        $menu
          .removeClass('active')
          .appendTo(document.body);
      }
    };

    var $overlayEl = $(mui.overlay('on', options));

    $menu.appendTo($overlayEl);
    setTimeout(function() {
      $menu.addClass('active');
    }, 20);
  }

  function hideMenu() {
    $body.toggleClass('hide-sidedrawer');
  }

  $('.js-show-sidedrawer').on('click', showMenu);
  $('.js-hide-sidedrawer').on('click', hideMenu);
});
