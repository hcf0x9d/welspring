// jscs:disable validateLineBreaks
// TODO: [Events calendar] -- think about parsing atom XML or iCal feeds (9)
// TODO: [Verse of the day] -- Easy to implement (3)
// TODO: [Service Guide] -- Phase 1 is a listing with links to websites/contact, Phase 2 built out a bit more... (4)
// TODO: [Banners] -- Consider banner ads for churches to post events, et cetera?  or businesses... (9)

var Model = function ( ) {

        this.object = {}

    },
    /**
     * Class for making a venue object
     *
     * @param obj - Google API object
     * @constructor
     */
    Venue = function ( obj ) {

        this.google_id = obj.google_id;
        this.id = obj.id;
        this.phone = obj.phone;
        this.address = obj.address;
        this.admin_name = obj.admin_name;
        this.livestream = obj.livestream;
        this.placeLoc = JSON.parse( obj.location );
        this.name = obj.name;
        this.slug = obj.slug;
        this.picture = obj.picture;
        this.type_id = obj.type_id;
        this.sub_type_id = obj.sub_type_id;
        this.state = obj.state;

    },
    /**
     * Welcome to the Google Maps portion of this, here's your class
     *
     * @constructor
     */
    MapBuilder = function () {

        var map,
            service,
            infowindow,
            venues = [],
            // Setting a default epicenter for the map
            pyrmont = { lat : 47.7987070, lng : -122.4981920, };

        geoLocate();

        $( '#mapSearch' ).on( 'change', function () {

            console.log( $( this ).val() );
            geoCodeSearch( $( this ).val() );

        } );

        /**
         * Initialization will first look for the user's location with HTML5
         * geolocation
         */
        function geoLocate () {

            // Try HTML5 geolocation.
            if ( navigator.geolocation ) {

                navigator.geolocation.getCurrentPosition( function ( position ) {

                    pyrmont = {
                        lat : position.coords.latitude,
                        lng : position.coords.longitude,
                    };

                    // Search here
                    initMap();

                }, function () {

                    // Error in location, run the search anyway (on initial
                    // pyrmont value
                    handleLocationError( true, infowindow, map.getCenter() );
                    initMap();

                } );

            } else {

                // Browser doesn't support Geolocation, run search on
                // initial pyrmont value
                handleLocationError( false, infowindow, map.getCenter() );
                initMap();

            }

        }

        function geoCodeSearch ( query ) {

            venues = [];

            $.ajax( {
                url      : '/api/geocode',
                type     : 'POST',
                data     : { search : query, },
                dataType : 'JSON',
            } ).success( function ( response ) {

                pyrmont = response.response;
                // map.center = pyrmont;
                initMap();

            } ).error( function ( response ) {

                console.log( response )

            } );

        }

        /**
         * Initialize the map and search for nearby locations
         */
        function initMap () {

            // Initialize the map
            map = new google.maps.Map( document.getElementById( 'map' ), {
                center          : pyrmont,
                zoom            : 10,
                gestureHandling : "cooperative",
                // FIXME: gestureHandling is not working
            } );

            service = new google.maps.places.PlacesService( map );

            // Initialize the infowindow variable
            infowindow = new google.maps.InfoWindow( {

            } );

            search();

        }

        function search () {

            $.ajax( {
                url      : '/api/venues',
                type     : 'POST',
                data     : { state : 'Washington', },
                dataType : 'JSON',
            } ).success( function ( results ) {

                for( var i = 0; i < results.response.length; i++ ) {

                    // Create a new instance of the Venue Class with this result
                    var venue = new Venue( results.response[i] );

                    // Add it to our array of venues
                    venues.push( venue );

                    createMarker( venue );

                }

                console.log( venues )

            } ).error( function ( response ) {

                console.log( response )

            } );

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
                    photo = '';

                // If we have a photo, build the element to house it
                if ( venue.picture !== null ) {

                    photo = '<img src="' + venue.picture +
                        '" alt="' + venue.name + '" height="100">';

                }

                // Build the infowindow inner element with all content
                content = '<div id="content">' +
                    '<header>' +
                        photo +
                        '<h1>' + venue.name + '</h1>' +
                    '</header>' +
                    '<div>' +
                        '<p>' + venue.address + '</p>' +
                        '<button class="js-map-details" data-id="' + venue.google_id + '" ' +
                            'data-slug="' + venue.slug + '">' +
                            'More info' +
                        '</button>' +
                    '</div>';

                infowindow.setContent( content );
                infowindow.open( map, this );

                $( '.js-map-details' ).on( 'click', function () {

                    getDetails( $( this ).data( 'id' ), $( this ).data( 'slug' ) );

                } );

            } );

        }

        function getDetails ( id, slug ) {

            // window.location.href = '/locator/site/' + id;
            $.ajax( {
                url      : '/api/place_details',
                type     : 'POST',
                data     : { id : id, slug : slug, },
                dataType : 'JSON',
            } ).success( function ( obj ) {

                infowindow.close();

                detailModal ( obj );

            } ).error( function ( response ) {

                console.log( response )

            } );

        }

        function detailModal ( obj ) {

            var $el = $( '.location-detail' ),
                gmap = obj.gmaps,
                welspring = obj.welspring;

            $( 'body' ).append( '<div class="shade"></div>' );

            console.log( gmap )

            // FIXME: This should be replaced with a better mechanism
            $el.find( '.location-header' ).css( 'background-image', 'url(' + welspring.picture + ')' );
            $el.find( '#locationName' ).html( welspring.name );
            $el.find( '#locationAddress' ).html( welspring.address );
            $el.find( '#locationSummary' ).html( welspring.summary );
            $el.find( '#locationLinkBtn' ).attr( 'href', welspring.website );
            $el.find( '#locationWebsite' ).attr( 'href', welspring.website )
                .text( welspring.website );
            $el.find( '#locationPhone' ).text( welspring.phone );
            $el.find( '#locationAdmin' ).text( welspring.admin );

            $( '.shade' ).fadeIn( 250, function () {

                $el.fadeIn( 250 );

            } );

            $( '.location-detail-close' ).on( 'click', function () {

                $( '.location-detail' ).fadeOut( 250, function () {

                    $( '.shade' ).fadeOut( 250, function () {

                        $( this ).remove();

                    } )

                } );

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
        return response;

    };

/**
 * Add New Item Class Constructor
 *
 * Instead of doing a post to open a window for adding a new item to a category
 * we will pop a lightbox for the user to add their input, then post that
 * information to the DB and refresh the same category view (reload)
 *
 * @constructor
 */
function AddNewVenue () {

    var _this = this;

    _this.address = null;
    _this.input = document.getElementById( 'venue_name' )
    _this.startButton = document.querySelector( '.js-new-venue' );

    /**
     * Inastead of requiring input, we can grab a lot from Google
     */
    _this.autocomplete = function () {

        var input = document.getElementById( 'venue_name' ),
            autocomplete = new google.maps.places.Autocomplete( input );

        autocomplete.setComponentRestrictions(
        { country : [ 'us', ], } );

        autocomplete.addListener( 'place_changed', function () {

            var place = autocomplete.getPlace(),
                obj = {},
                loc = {
                    lat : place.geometry.location.lat(),
                    lng : place.geometry.location.lng(),
                };

            obj.name = place.name;
            obj.website = place.website;
            obj.address = place.adr_address;
            obj.google_id = place.place_id;
            obj.phone = place.formatted_phone_number;
            // language=JSRegexp
            obj.slug = place.name.replace( /[^A-Za-z0-9]+/g, "-" ).toLowerCase();
            obj.location = JSON.stringify( loc );

            $.ajax( {
                url  : '/create/venue',
                type : 'POST',
                data : obj,
            } )
            .done( function ( response ) {

                response = JSON.parse( response );
                console.log( response );
                window.location.reload();

            } )
            .fail( function () {

                swal( 'Oops...', 'Something went wrong with ajax!', 'error' );

            } );

        } );

    }

    // Kick off the handler
    _this.autocomplete();

}

function UpdateVenue () {

    var _this = this;

    _this.init = function () {

        $( '.js-radio' ).on( 'change', function ( e ) {

            $.ajax( {
                url  : '/api/getVenueSubTypes',
                type : 'POST',
                data : { id : this.value, },
            } )
            .done( function ( response ) {

                var opts, keys,
                    options = '<option value="">Select an option</option>';

                response = JSON.parse( response );
                opts = response.response;

                keys = Object.keys( opts );

                for( i = 0; i < keys.length; i++ ) {

                    options += '<option value="' + opts[keys[i]] + '">' + keys[i] + '</option>';

                }

                $( '#v_edit_subtype' ).empty().append( options );

                _this.edit();

            } )
            .fail( function () {

                swal( 'Oops...', 'Something went wrong with ajax!', 'error' );

            } );

        } );

        $( 'select.venue-input' ).on( 'change', function () {

            // console.log( $( this ).find( 'option:selected' ).val() )

            _this.edit()

        } )

    }

    _this.change = function () {

        $( '.venue-input' ).on( 'change', function ( e ) {

            e.preventDefault();

            _this.edit();

        } );

    }

    _this.edit = function () {

        var form = objectifyForm( $( '#venue_update_form' ).serializeArray() );

        console.log( form );

        $.ajax( {
            url  : '/update/venue',
            type : 'POST',
            data : form,
        } )
        .done( function ( response ) {

            // TODO: Notice that says "this has happened"
            console.log( response )

        } )
        .fail( function () {

            swal( 'Oops...', 'Something went wrong with ajax!', 'error' );

        } );

    }

}

function objectifyForm ( formArray ) {

    var returnArray = {};
    for( var i = 0; i < formArray.length; i++ ) {

        returnArray[formArray[ i ].name ] = formArray[ i ].value;

    }
    return returnArray;

}
