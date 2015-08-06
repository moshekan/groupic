function loadEvent(id){
    console.log("Load Events " + id);
	//Put loading symbol
    //TODO

	//Make ajax request
	$.ajax( "/view_images?event_id="+id)
  		.success(function(eventOb) {
  		    //When ajax request ends- loadPhotos(photos)
    		loadPhotos(eventOb.media);
            $("#photosGallery").show();


            initPhotoSwipeFromDOM('#photosGallery');    
            $(".backbtn").show();

            id = id.replace(/-/g, " ");
            $(".header1").html(id);


  		})
        .fail(function() {
            console.log("Error");
        });




}
function loadPhotos(photos){
	//Throw away the events except the one we loaded - (keep them)
	$("#eventsGallery").hide();
	
	$(".eventPhotoElement").remove();

	//create elements for images underneat main
	for(var i = 0; i < photos.length; i++){
		$( "#photosGallery" ).append( getPhotoElement(photos[i].thumbnail, photos[i].username, photos[i].full_res));
	}
	$("#photosGallery").show();
	//animate these images

	//Back button element unhide

	initPhotoSwipeFromDOM('#photosGallery');	
}

function goBack(){
	$("#photosGallery").hide();
	//Make photosgo back into event
	$(".eventsGallery").show();
	//Load back events
    $(".backbtn").hide();
}


function getPhotoElement(thumbnailurl, caption, fullimage){
	return '<figure id="arrange" class="eventPhotoElement" itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject"><a itemprop="contentUrl" data-size="600x400"><img fullimageurl="'+fullimage+'" src="'+thumbnailurl+'" itemprop="thumbnail" alt="Image description" /></a><figcaption itemprop="'+caption+'">'+caption+'</figcaption></figure>';
}

var initPhotoSwipeFromDOM = function(gallerySelector) {

    // parse slide data (url, title, size ...) from DOM elements 
    // (children of gallerySelector)
    var parseThumbnailElements = function(el) {
        var thumbElements = el.childNodes,
            numNodes = thumbElements.length,
            items = [],
            figureEl,
            linkEl,
            size,
            item;

        for(var i = 1; i < numNodes; i++) {

            figureEl = thumbElements[i]; // <figure> element

            // include only element nodes 
            if(figureEl.nodeType !== 1) {
                continue;
            }

            linkEl = figureEl.children[0]; // <a> element

            size = linkEl.getAttribute('data-size').split('x');

            // create slide object
            item = {
                src: figureEl.getAttribute("fullimageurl"),
                w: parseInt(size[0], 10),
                h: parseInt(size[1], 10)
            };



            if(figureEl.children.length > 1) {
                // <figcaption> content
                item.title = figureEl.children[1].innerHTML; 
            }

            if(linkEl.children.length > 0) {
                // <img> thumbnail element, retrieving thumbnail url
                item.src = linkEl.children[0].getAttribute('fullimageurl');
            } 

            item.el = figureEl; // save link to element for getThumbBoundsFn
            items.push(item);
        }
        console.log(items);
        return items;
    };

    // find nearest parent element
    var closest = function closest(el, fn) {
        return el && ( fn(el) ? el : closest(el.parentNode, fn) );
    };

    // triggers when user clicks on thumbnail
    var onThumbnailsClick = function(e) {
        e = e || window.event;
        e.preventDefault ? e.preventDefault() : e.returnValue = false;

        var eTarget = e.target || e.srcElement;

        // find root element of slide
        var clickedListItem = closest(eTarget, function(el) {
            return (el.tagName && el.tagName.toUpperCase() === 'FIGURE');
        });

        if(!clickedListItem) {
            return;
        }

        // find index of clicked item by looping through all child nodes
        // alternatively, you may define index via data- attribute
        var clickedGallery = clickedListItem.parentNode,
            childNodes = clickedListItem.parentNode.childNodes,
            numChildNodes = childNodes.length,
            nodeIndex = 0,
            index;

        for (var i = 0; i < numChildNodes; i++) {
            if(childNodes[i].nodeType !== 1) { 
                continue; 
            }

            if(childNodes[i] === clickedListItem) {
                index = nodeIndex;
                break;
            }
            nodeIndex++;
        }



        if(index >= 0) {
            // open PhotoSwipe if valid index found
            openPhotoSwipe( index, clickedGallery );
        }
        return false;
    };

    // parse picture index and gallery index from URL (#&pid=1&gid=2)
    var photoswipeParseHash = function() {
        var hash = window.location.hash.substring(1),
        params = {};

        if(hash.length < 5) {
            return params;
        }

        var vars = hash.split('&');
        for (var i = 0; i < vars.length; i++) {
            if(!vars[i]) {
                continue;
            }
            var pair = vars[i].split('=');  
            if(pair.length < 2) {
                continue;
            }           
            params[pair[0]] = pair[1];
        }

        if(params.gid) {
            params.gid = parseInt(params.gid, 10);
        }

        return params;
    };

    var openPhotoSwipe = function(index, galleryElement, disableAnimation, fromURL) {
        var pswpElement = document.querySelectorAll('.pswp')[0],
            gallery,
            options,
            items;

        items = parseThumbnailElements(galleryElement);

        // define options (if needed)
        options = {

            // define gallery index (for URL)
            galleryUID: galleryElement.getAttribute('data-pswp-uid'),

            getThumbBoundsFn: function(index) {
                // See Options -> getThumbBoundsFn section of documentation for more info
                var thumbnail = items[index].el.getElementsByTagName('img')[0], // find thumbnail
                    pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                    rect = thumbnail.getBoundingClientRect(); 

                return {x:rect.left, y:rect.top + pageYScroll, w:rect.width};
            }

        };

        // PhotoSwipe opened from URL
        if(fromURL) {
            if(options.galleryPIDs) {
                // parse real index when custom PIDs are used 
                // http://photoswipe.com/documentation/faq.html#custom-pid-in-url
                for(var j = 0; j < items.length; j++) {
                    if(items[j].pid == index) {
                        options.index = j;
                        break;
                    }
                }
            } else {
                // in URL indexes start from 1
                options.index = parseInt(index, 10) - 1;
            }
        } else {
            options.index = parseInt(index, 10);
        }

        // exit if index not found
        if( isNaN(options.index) ) {
            return;
        }

        if(disableAnimation) {
            options.showAnimationDuration = 0;
        }

        // Pass data to PhotoSwipe and initialize it
        gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
    };

    // loop through all gallery elements and bind events
    var galleryElements = document.querySelectorAll( gallerySelector );

    for(var i = 0, l = galleryElements.length; i < l; i++) {
        galleryElements[i].setAttribute('data-pswp-uid', i+1);
        galleryElements[i].onclick = onThumbnailsClick;
    }

    // Parse URL and open gallery if it contains #&pid=3&gid=1
    var hashData = photoswipeParseHash();
    if(hashData.pid && hashData.gid) {
        openPhotoSwipe( hashData.pid ,  galleryElements[ hashData.gid - 1 ], true, true );
    }
};

$(document).ready(function() {
    $(".click").click(function() {
        var id = $(this).attr("id");
        loadEvent(id);
    });
});

function SearchEvents(str) {
    // alert("sumtin sexy happened");
    // var divs = document.getElementsByClassName("helpSearch");
    // for(var i = 0; i < divs.length; i++){
    //     var n = divs[i].innerHTML.toUpperCase().search(str.toUpperCase());
    //     if (n > -1) {
    //         divs[i].innerHTML("bla") = ""
    //         alert("yes " + divs[i].innerHTML + " " + n);
    //     }
    // }
}

// function wordInString(s, word){
//     return new RegExp( '\\b' + word + '\\b', 'i').test(s);
// }

function Start() {
    $(".container").show();
    $(".color-bar-1").show();
    $(".color-bar-2").show();
    $("#landing").css({
        position : "absolute",
        zIndex : "1000"});
    $("#landing").animate({
        top : "-100%"
    }, 2000);
    var expiration_date = new Date();
    var cookie_string = '';
    expiration_date.setFullYear(expiration_date.getFullYear() + 1);
    // Build the set-cookie string:
    cookie_string = "landing=true; path=/; expires=" + expiration_date.toGMTString();
    document.cookie = cookie_string;
    // $(".container").css({position : "absolute"});
    // $(".container").animate({
    //     top : "0"
    // }, 3000);
    // $("#landing").delay(3000).hide();
}

// function Hide() {
//     $(".container").hide();
//     $(".color-bar-1").hide();
//     $(".color-bar-2").hide();
// }

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    return unescape(dc.substring(begin + prefix.length, end));
} 

function doSomething() {
    var myCookie = getCookie("landing");

    if (myCookie == "true") {
        $("#landing").hide();
    }else{
        $("#landing").show();
        $(".container").hide();
        $(".color-bar-1").hide();
        $(".color-bar-2").hide();
    }
}
    $(document).ready(function() {

  var active1 = false;
  var active2 = false;
  var active3 = false;
  var active4 = false;

    $('.parent2').on('mousedown touchstart', function() {
    
    if (!active1) $(this).find('.test1').css({'background-color': 'gray', 'transform': 'translate(0px,125px)'});
    else $(this).find('.test1').css({'background-color': 'dimGray', 'transform': 'none'}); 
     if (!active2) $(this).find('.test2').css({'background-color': 'gray', 'transform': 'translate(-60px,105px)'});
    else $(this).find('.test2').css({'background-color': 'darkGray', 'transform': 'none'});
      if (!active3) $(this).find('.test3').css({'background-color': 'gray', 'transform': 'translate(-105px,60px)'});
    else $(this).find('.test3').css({'background-color': 'silver', 'transform': 'none'});
      if (!active4) $(this).find('.test4').css({'background-color': 'gray', 'transform': 'translate(-125px,0px)'});
    else $(this).find('.test4').css({'background-color': 'silver', 'transform': 'none'});
    active1 = !active1;
    active2 = !active2;
    active3 = !active3;
    active4 = !active4;
      
    });
});
