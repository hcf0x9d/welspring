// jscs:disable validateLineBreaks
// TODO: [Events calendar] -- think about parsing atom XML or iCal feeds (9)
// TODO: [Verse of the day] -- Easy to implement (3)
// TODO: [Service Guide] -- Phase 1 is a listing with links to websites/contact, Phase 2 built out a bit more... (4)
// TODO: [Banners] -- Consider banner ads for churches to post events, et cetera?  or businesses... (9)

/**
 * Class for making a venue object
 *
 * @param obj - Google API object
 * @constructor
 */
var Venue = function ( obj ) {

    this.placeLoc = obj.geometry.location;
    this.name = obj.name;
    this.photos = obj.photos;
    this.types = obj.types;
    this.vicinity = obj.vicinity;

},
    /**
     * Welcome to the Google Maps portion of this, here's your class
     *
     * @constructor
     */
    MapBuilder = function () {

        var map,
            infowindow,
            venues = [],
            // Setting a default epicenter for the map
            pyrmont = { lat : 47.7987070, lng : -122.4981920, };

        initMap();

        /**
         * Initialization will first look for the user's location with HTML5
         * geolocation
         */
        function initMap () {

            // Try HTML5 geolocation.
            if ( navigator.geolocation ) {

                navigator.geolocation.getCurrentPosition( function ( position ) {

                    pyrmont = {
                        lat : position.coords.latitude,
                        lng : position.coords.longitude,
                    };

                    // Search here
                    search();

                }, function () {

                    // Error in location, run the search anyway (on initial
                    // pyrmont value
                    handleLocationError( true, infowindow, map.getCenter() );
                    search();

                } );

            } else {

                // Browser doesn't support Geolocation, run search on
                // initial pyrmont value
                handleLocationError( false, infowindow, map.getCenter() );
                search();

            }

        }

        /**
         * Initialize the map and search for nearby locations
         */
        function search () {

            // Initialize the map
            map = new google.maps.Map( document.getElementById( 'map' ), {
                center : pyrmont,
                zoom   : 10,
            } );

            // Initialize the infowindow variable
            infowindow = new google.maps.InfoWindow( {

                maxWidth : 200,

            } );

            // Search for the places
            var service = new google.maps.places.PlacesService( map );
            service.nearbySearch( {
                location : pyrmont,
                radius   : 40000,
                keyword  : [ 'WELS', 'ELS', ],
                // TODO: Replace the type with the url value
                // either church, school or search for church by default
                type     : [ 'church', ],
            }, callback );

        }

        /**
         * Error in Geolocation
         *
         * @param browserHasGeolocation - Boolean
         * @param infowindow - infowindow object
         * @param pos
         */
        function handleLocationError ( browserHasGeolocation, infowindow, pos ) {

            infowindow.setPosition( pos );
            infowindow.setContent( browserHasGeolocation ?
                                  'Error: The Geolocation service failed.' :
                                  'Error: Your browser doesn\'t support geolocation.' );
            infowindow.open( map );

        }

        /**
         * Search complete, do something with the results
         * @param results
         * @param status
         */
        function callback ( results, status ) {

            if ( status === google.maps.places.PlacesServiceStatus.OK ) {

                for( var i = 0; i < results.length; i++ ) {

                    // Create a new instance of the Venue Class with this result
                    var venue = new Venue( results[i] );

                    // Add it to our array of venues
                    venues.push( venue );

                    createMarker( venue );

                }

            }

        }

        /**
         * Make the map marker
         * @param venue
         */
        function createMarker ( venue ) {

            var marker = new google.maps.Marker( {
                map      : map,
                position : venue.placeLoc,
            } );

            // Handling clicks of the markers to show the infowindow
            google.maps.event.addListener( marker, 'click', function () {

                var content,
                    photo = '',
                    type = [];

                // Make the types legible and not in an array
                for( var i = 0; i < venue.types.length; i++ ) {

                    if ( venue.types[i] === 'church' || venue.types[i] === 'school' ) {

                        type.push( venue.types[i] );

                    }

                }

                // If we have a photo, build the element to house it
                if ( venue.photos !== undefined ) {

                    photo = '<img src="' + venue.photos[0].getUrl( { maxWidth : 200, maxHeight : 100, } ) +
                        '" alt="' + venue.name + '" height="100">';

                }

                // Build the infowindow inner element with all content
                content = '<div id="content">' +
                    '<header>' +
                        photo +
                        '<h1>' + venue.name + '</h1>' +
                    '</header>' +
                    '<div>' +
                        '<p>' + type.join( ', ' ) + '</p>' +
                        '<p>' + venue.vicinity + '</p>' +
                    '</div>';

                infowindow.setContent( content );
                infowindow.open( map, this );

            } );

        }

    };

/**
 * Error occurred with the map
 * @param response
 * @returns {*}
 */
MapBuilder.prototype.error = function ( response ) {

        // TODO: Need to handle this I guess.
        return response

    };

// Initialize the app
$( function () {

    controller.init();

} );
