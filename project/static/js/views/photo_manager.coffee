define [
  'cs!views/manager/album_editor'
  'cs!views/manager/photo_feed'
  'cs!collections/user_albums'
  'cs!views/manager/uploader'
], (AlbumEditor, PhotoManagerFeed, UserAlbums, Uploader) ->
  class PhotoManager extends Backbone.View
    el: '#photo-manager'

    events:
      'click .delete-link': 'delete_photos'

    initialize: ->
      @uploader = new Uploader({@collection})
      collection = new UserAlbums
      @album_editor = new AlbumEditor({collection})
      @photo_feed = new PhotoManagerFeed({@collection})

    delete_photos: (event) ->
      event.preventDefault()
      @photo_feed.delete_selected_photos()
