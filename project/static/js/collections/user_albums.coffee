define ['cs!models/user_album'], (UserAlbum) ->
  class UserAlbums extends Backbone.Collection
    url: '/api/albums'
    model: UserAlbum
