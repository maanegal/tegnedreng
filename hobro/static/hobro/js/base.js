(function () { lazyload = new LazyLoad({ elements_selector: '.lazy', });}());
document.addEventListener('DOMContentLoaded', () => {
//window.onload = function(){


    var showAnim = showAnimations();
    if (showAnim) {
        sal({threshold: 0.1});
    }
//}
});




    document.getElementById('menuSettings').addEventListener('click', function() {
        toggleShowMenu();
        modalOpen('settings-modal');
    });

    document.getElementById('menuStory').addEventListener('click', function() {
        toggleShowMenu();
        modalOpen('story-modal');
    });

document.getElementById("switchAnim").addEventListener("click", setAnimPref);
document.getElementById("playerSP").addEventListener("click", setPlayerPref);
document.getElementById("playerBC").addEventListener("click", setPlayerPref);
document.getElementById("commentOff").addEventListener("click", setCommentPref);
document.getElementById("commentOn").addEventListener("click", setCommentPref);
document.getElementById("commentToggle").addEventListener("click", setCommentPref);
document.getElementById("switchBook").addEventListener("click", setBookPref);

var cookieBanner = document.getElementById('the-cookies');
var cookieBtn = document.getElementById('cookie-okay');
cookieBtn.addEventListener('click', function() {
    setCookie('cookie_consent', "true", 365);
    cookieBanner.classList.remove('is-active');
});

var bm = getBookmark();
if (bm == "off") {
    var bookOnM = document.getElementById('bookmark-activate');
    bookOnM.addEventListener('click', function() {
        bookOnM.innerHTML = '<span class="icon is-small"><i class="fas fa-check"></i></span><span>Bogmærke gemmes nu</span></a>';
        document.getElementById("switchBook").checked = true;
        setCookie('bookmark', "", 14);
        setTimeout(function(){
            location.reload();
        },300);
    });
} else if (bm) {
    document.getElementById('bookmark-go-menu').addEventListener('click', function() {
        modalClose('story-modal');
        location = "/kapitel/" + bm[0] + "/#" + bm[1];
    });
}