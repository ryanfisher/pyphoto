class AlbumPhotos extends Backbone.Collection
  # Uses default ordering for albums
  url: '/api/photos'
  model: UserPhoto
