class UserAlbum extends Backbone.Model

  parse: (response, options) ->
    photos = new AlbumPhotos(response['photos'])
    response['photos'] = photos
    super(response, options)
