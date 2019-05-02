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

function setBookPref() {
    var pref = document.getElementById("switchBook");
    if (pref.checked) { var s = ""; } else { var s = "off"; }
    setCookie('bookmark', s, 14);
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


function disableScroll() {
    var htmlElement = document.querySelector("html");
    htmlElement.classList.add('locked');
}

function enableScroll() {
    var htmlElement = document.querySelector("html");
    htmlElement.classList.remove('locked');
}


function toggleShowMenu() {
    var sideMenu = document.getElementById("sideMenu");
    var menuOverlay = document.getElementById("menuOverlay");
    var menuButton = document.getElementById("menuButton");
    menuButton.classList.toggle('is-active');
    sideMenu.classList.toggle('is-active');
    menuOverlay.classList.toggle('is-active');
    if (sideMenu.classList.contains('is-active')) {
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
                toggleShowMenu();
            }
        };
    } else {
        enableScroll();
        document.onkeyup = null;
    }
}

function modalOpen(modalId) {
    var modal = document.getElementById(modalId);
    modal.classList.add('prepare');
    setTimeout(function(){
        modal.classList.add('is-active');
   },20);
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
    modal.classList.remove('is-active');
    enableScroll();
    document.onkeyup = null;
}

function commentToggle(comId, btnId, closerId, scroll=false) {
    var comment = document.getElementById(comId);
    var button = document.getElementById(btnId);
    var closer = document.getElementById(closerId);
    var w = 300;
    if (!showAnimations()) { comment.classList.add('no-motion'); w = 30; }
    button.style.visibility = "visible";
    if ( comment.classList.contains('collapsed') ) {
        comment.classList.remove('disappeared');
        setTimeout(function(){
            comment.classList.remove('collapsed');
        },30);
        closer.style.display = "block";
        button.innerHTML = '<i class="fas fa-angle-double-up"></i>&nbsp;&nbsp;Skjul kommentar';
    } else {
        comment.classList.add('collapsed');
        setTimeout(function(){
            comment.classList.add('disappeared');
        },w);
        closer.style.display = "none";
        button.innerHTML = '<i class="fas fa-angle-double-down"></i>&nbsp;&nbsp;Vis kommentar';
        if (scroll) {
            setTimeout(function(){
            comment.scrollIntoView({block: "start", behavior: "smooth"});
            },50);
        }
    }
}

function motifToggle(motifId, commentId) {
    var motif = document.getElementById(motifId+'-'+commentId);
    var button = document.getElementById('head-'+motifId+'-'+commentId);
    var head = button.querySelector('.motif-head-right');
    var w = 300;
    if (!showAnimations()) { motif.classList.add('no-motion'); w = 30; }
    if ( motif.classList.contains('collapsed') ) {
        motif.classList.remove('disappeared');
        setTimeout(function(){
            motif.classList.remove('collapsed');
        },30);
        head.innerHTML = '<span><i class="fas fa-angle-double-up"></i></span>';
    } else {
        motif.classList.add('collapsed');
        setTimeout(function(){
            motif.classList.add('disappeared');
        },w);
        head.innerHTML = '<span><i class="fas fa-angle-double-down"></i></span>';
    }
}

function filterList(queryField, queryList) {
  // from w3schools
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById(queryField);
  filter = input.value.toUpperCase();
  ul = document.getElementById(queryList);
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

function clearText(queryField, queryList="") {
    document.getElementById(queryField).value = "";
    if (queryList) {
      ul = document.getElementById(queryList);
      li = ul.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        li[i].style.display = "";
      }
    }
}

function reload_iframes() {
    var f_list = document.getElementsByTagName('iframe');
    for (var i = 0, f; f = f_list[i]; i++) { f.src = f.src; }
}

function getBookmark() {
    var bookVal = getCookie("bookmark");
    if (bookVal) {
        if (bookVal == "off") { return "off";
        //} else if (bookVal.length === 0) { return "";
        } else {
        // determine if val seems valid, return in two parts
        var vals = bookVal.split("/")
        if (vals.length == 2) {
            var chp = vals[0];
            var elem = vals[1];
            if (/^\d+$/.test(chp) || /^\d+$/.test(elem)) { //test if they're only numbers
                return [chp, elem];
                }
            }
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.nav-toggle'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach($el => {
      $el.addEventListener('click', toggleShowMenu);
    });
  }

    var killPlayers = document.getElementsByClassName("killPlayers");
    for (var i = 0; i < killPlayers.length; i++) {
        killPlayers[i].addEventListener("click", function() {
            reload_iframes();
        });
    }
});
