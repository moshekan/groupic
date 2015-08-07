$(".json").hide();
$(".backbtn").hide();
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
            $(".backbtn").show();

            $('.eventPhotoElement').each(function(i) {
                $(this).children().children().css({ opacity : "0"}).delay(400*i).animate({ opacity : "1"})
            });


            initPhotoSwipeFromDOM('#photosGallery');

            id = id.replace(/-/g, " ");
            $(".header1").html(id);

            $(".section-title").hide();

            // refresh = true;


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
        if (i == 0) {

        };
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
    return '<figure id="arrange" class="eventPhotoElement" itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject"><a itemprop="contentUrl" data-size="600x400"><img fullimageurl="'+fullimage+'" src="'+thumbnailurl+'" itemprop="thumbnail" alt="Image description" class="img-thumbnail thumb" /></a><!-- <figcaption class="animate" itemprop="'+caption+'">'+caption+'</figcaption> --></figure>';
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
            openPhotoSwipe( index-1, clickedGallery );
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

$(".backbtn").click(function() {
    $("#photosGallery").hide();
    $("json").hide();
    $(".eventPhotoElement").hide();
    $(".section-title").show();
    $(".backbtn").hide();
    $(".header1").hide();
    $("#eventsGallery").show();
});

(function(){
    var now = Math.floor(Date.now() / 1000);
    console.log("send to server " + now);
    newImages(now);
    setTimeout(arguments.callee, 10000);
})();

function newImages(now) {
    //send request to server with {now} and server return images with timestamp > {now}
    var images = requestImagesFromServer(now);
    //transform from json to html
    writeToHTML(images);
}

function requestImagesFromServer (now) {
    // ask server for images bigger than {now}
    return [{
    "created_time": 1406235540,
    "full_res": "http://static.dnaindia.com/sites/default/files/2015/06/26/349928-paolo-gurrero-peru-reuters-crop.jpg",
    "like_count": 9,
    "location": "",
    "tags": ["copaamerica", "copa_america2015"],
    "thumbnail": "http://static.dnaindia.com/sites/default/files/2015/06/22/348687-reuters-copa-america-thiago-silva.jpg",
    "username": "2"
}, {
    "created_time": 1406235540,
    "full_res": "http://static.dnaindia.com/sites/default/files/2015/07/06/353041-leo-messi-after-copa-america-final-afp-crop.jpg",
    "like_count": 9,
    "location": "",
    "tags": ["copaamerica", "copa_america2015"],
    "thumbnail": "http://static.dnaindia.com/sites/default/files/2015/07/06/353041-leo-messi-after-copa-america-final-afp-crop.jpg",
    "username": "3"
}, {
    "created_time": 1406235540,
    "full_res": "http://static.dnaindia.com/sites/default/files/2015/06/20/348098-afp-copa-america-chile-bolivia-ed.jpg",
    "like_count": 9,
    "location": "",
    "tags": ["copaamerica", "copa_america2015"],
    "thumbnail": "http://static.dnaindia.com/sites/default/files/2015/06/20/348098-afp-copa-america-chile-bolivia-ed.jpg",
    "username": "4"
}, {
    "created_time": 1406235540,
    "full_res": "http://static.dnaindia.com/sites/default/files/2015/07/09/354106-argentina-team.jpg",
    "like_count": 9,
    "location": "",
    "tags": ["copaamerica", "copa_america2015"],
    "thumbnail": "http://static.dnaindia.com/sites/default/files/2015/07/09/354106-argentina-team.jpg",
    "username": "5"
}, {
    "created_time": 1406235540,
    "full_res": "http://static.dnaindia.com/sites/default/files/2015/06/27/350236-carlos-tevez-reuters-crop.jpg",
    "like_count": 9,
    "location": "",
    "tags": ["copaamerica", "copa_america2015"],
    "thumbnail": "http://static.dnaindia.com/sites/default/files/2015/06/27/350236-carlos-tevez-reuters-crop.jpg",
    "username": "6"
}]
}

function writeToHTML (images) {
    // Json to html
    for (var i = 0; i <= images.length - 1; i++) {
        var fullimage = images[i].full_res
        var thumbnailurl = images[i].thumbnail
        var caption = images[i].username
        $( "#photosGallery" ).prepend('<figure id="arrange" class="eventPhotoElement" itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject"><a itemprop="contentUrl" data-size="600x400"><img fullimageurl="'+fullimage+'" src="'+thumbnailurl+'" itemprop="thumbnail" alt="Image description" class="img-thumbnail thumb" /></a><!-- <figcaption class="animate" itemprop="'+caption+'">'+caption+'</figcaption> --></figure>');
        console.log('<figure id="arrange" class="eventPhotoElement" itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject"><a itemprop="contentUrl" data-size="600x400"><img fullimageurl="'+fullimage+'" src="'+thumbnailurl+'" itemprop="thumbnail" alt="Image description" class="img-thumbnail thumb" /></a><!-- <figcaption class="animate" itemprop="'+caption+'">'+caption+'</figcaption> --></figure>');
    };
    console.log("writeToHTML");
}