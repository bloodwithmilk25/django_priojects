$(document).ready(function() {
  $('li.nav-item.px-2.active').removeClass('active');
  $('a[href="' + location.pathname + '"]').closest('li').addClass('active');
});