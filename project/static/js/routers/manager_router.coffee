define [
  'cs!collections/user_photos'
  'cs!views/photo_manager'
], (UserPhotos, PhotoManager) ->
  class ManagerRouter extends Backbone.Router

    routes:
      'upload': 'open_uploader'
      'albums': 'open_album_editor'

    open_uploader: ->
      $('#photo-manager').trigger('open_uploader')

    open_album_editor: ->
      $('#photo-manager').trigger('open_album_editor')
