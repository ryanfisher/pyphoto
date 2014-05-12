define ['cs!models/user_photo'], (UserPhoto) ->
  class UserPhotos extends Backbone.Collection
    url: '/api/photos'
    model: UserPhoto
