
function decorateInfoWindow(regulation_id, description) {
    var info =  '<div id="content">' + '<h1 id="regulation_id">' + regulation_id + '</h1>'+ '<div id="bodyContent">'+ description + '</div>' + ' </div>';

    return info;
}
