class UserAlbum extends Backbone.Model

  parse: (response, options) ->
    photos = new UserPhotos(response['photos'])
    response['photos'] = photos
    super(response, options)
