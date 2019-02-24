/* Cookie cutter cookie code from the w3 school */
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function showAnimations() {
  var anim = getCookie("show_animations");
  if (anim == "false") { return false;
  } else { return true; }
}

function usePlayer() {
  var player = getCookie("use_player");
  if (player == "spotify") { return false;
  } else { return true; }
}

function showComments() {
  var player = getCookie("show_comments");
  if (player == "on") { return 1;
  } else if (player == "off") { return 2;
  } else { return 0; }
}


function setAnimPref() {
    var pref = document.getElementById("switchAnim");
    setCookie('show_animations', pref.checked, 14);
}

function setPlayerPref() {
    var bc = document.getElementById('playerBC');
    var sp = document.getElementById('playerSP');
    if (sp.checked) {
        setCookie('use_player', 'spotify', 30);
    } else {
        setCookie('use_player', 'bandcamp', 30);
    }
}

function setCommentPref() {
    var comOn = document.getElementById('commentOn');
    var comOff = document.getElementById('commentOff');
    var comTog = document.getElementById('commentToggle');
    if (comOn.checked) {
        setCookie('show_comments', 'on', 30);
    } else if (comOff.checked) {
        setCookie('show_comments', 'off', 30);
    } else {
        setCookie('show_comments', 'toggle', 30);
    }
}


document.addEventListener('DOMContentLoaded', () => {
    var anim = showAnimations();
    var klaus = document.getElementsByTagName("nav");
    if ( anim ) { Velocity(klaus, { opacity: [1, 0] }, {duration: 1000, easing: 'ease-in'} ); }
//Velocity(klaus, { opacity: [1, 0] }, {duration: 1000, easing: 'ease-in'} );

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach($el => {
      $el.addEventListener('click', function () {

        // Get the target from the "data-target" attribute
        const target = $el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the class on both the "navbar-burger" and the "navbar-menu"
        $el.classList.toggle('is-active');
        //$target.classList.toggle('is-active');
        var sideMenu = document.getElementById("sideMenu");
        var anim = showAnimations();
        if (anim) {
            if (sideMenu.style.display === "none") {
                Velocity(sideMenu, { transform: [ "translate(0)", "translate(100%)" ], opacity: [ 1, 0 ], display: ['block', 'none'] }, 150, "ease-out")
            } else {
                Velocity(sideMenu, { transform: ["translate(100%)", "translate(0)"], opacity: [ 0, 1 ], display: ['none', 'block'] }, 150, "ease-in")
            }
         } else {
            if (sideMenu.style.display === "none") {
                sideMenu.style.display = "block";
            } else { sideMenu.style.display = "none"; }
             $target.classList.add('is-active'); }
      });
    });
  }
});


// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e = e || window.event;
  if (e.preventDefault)
      e.preventDefault();
  e.returnValue = false;
}

function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
        preventDefault(e);
        return false;
    }
}

function disableScroll() {
  if (window.addEventListener) // older FF
      window.addEventListener('DOMMouseScroll', preventDefault, false);
  window.onwheel = preventDefault; // modern standard
  window.onmousewheel = document.onmousewheel = preventDefault; // older browsers, IE
  window.ontouchmove  = preventDefault; // mobile
  document.onkeydown  = preventDefaultForScrollKeys;
}

function enableScroll() {
    if (window.removeEventListener)
        window.removeEventListener('DOMMouseScroll', preventDefault, false);
    window.onmousewheel = document.onmousewheel = null;
    window.onwheel = null;
    window.ontouchmove = null;
    document.onkeydown = null;
}


function modalOpen(modalId) {
    var modal = document.getElementById(modalId);
    modal.classList.add('activated');
    var anim = showAnimations();
    if (anim) {
        Velocity(modal, { opacity: [1, 0], display: 'flex' }, {duration: 300, easing: 'ease-in'} );
    } else {
        modal.style.opacity = "1";
        modal.style.display = "flex";
    }
    disableScroll();
    document.onkeyup = function(evt) {
        evt = evt || window.event;
        var isEscape = false;
        if ("key" in evt) {
            isEscape = (evt.key === "Escape" || evt.key === "Esc");
        } else {
            isEscape = (evt.keyCode === 27);
        }
        if (isEscape) {
            modalClose(modalId);
        }
    };
}
function modalClose(modalId) {
    var modal = document.getElementById(modalId);
    modal.classList.remove('activated');
    var anim = showAnimations();
    if (anim) {
        Velocity(modal, { opacity: [0, 1], display: 'none' }, {duration: 300, easing: 'ease-out'} );
    } else {
        modal.style.opacity = "0";
        modal.style.display = "none";
    }
    enableScroll();
    document.onkeyup = null;
}

function commentToggle(comId, btnId) {
    var comment = document.getElementById(comId);
    var button = document.getElementById(btnId);
    var anim = showAnimations();
    if ( comment.classList.contains('collapsed') ) {
        if (anim) {
            Velocity(comment, { transform: [ "translateY(0)", "translateY(-30%)" ], opacity: [1, 0], display: 'flex' }, {duration: 400, easing: 'ease-out'} );
        } else {
            comment.style.opacity = "1";
            comment.style.display = "flex";
        }
        comment.classList.remove('collapsed');
        button.innerHTML = '&and;&nbsp;&nbsp;Skjul kommentarspor';
    } else {
        if (anim) {
            Velocity(comment, { transform: [ "translateY(-30%)", "translateY(0%)" ], opacity: [0, 1], display: 'none' }, {duration: 300, easing: 'ease-in'} );
        } else {
            comment.style.opacity = "0";
            comment.style.display = "none";
        }
        comment.classList.add('collapsed');
        button.innerHTML = '&or;&nbsp;&nbsp;Vis kommentarspor';
    }

}

window.onload = function() {
    var h = document.documentElement,
      b = document.body,
      st = 'scrollTop',
      sh = 'scrollHeight',
      progress = document.querySelector('.progress-bar'),
      scroll;

    document.addEventListener('scroll', function() {
      scroll = (h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight) * 100;
      progress.style.setProperty('--scroll', scroll + '%');
    });
}