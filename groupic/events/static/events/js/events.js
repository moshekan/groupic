function loadEvent(id){
	//Put loading symbol

	//Make ajax request
	$.ajax( "/ASKJOSH" )
  .done(function(eventsArray) {
  	//When ajax request ends- loadPhotos(photos)
    loadPhotos(eventsArray);
  })
  .fail(function() {
    console.log("Error");
  });
	

}
loadPhotos("eee");
function loadPhotos(photos){
	alert(photos);
	//Throw away the events except the one we loaded - (keep them)

	//create elements for images underneat main

	//animate these images

	//Back button element unhide

}

function goBack(){
	//Make photosgo back into event

	//Load back events
}