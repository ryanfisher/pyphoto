define [
  'cs!collections/user_photos'
  'cs!views/photo_manager'
], (UserPhotos, PhotoManager) ->
  class ManagerRouter extends Backbone.Router

    routes:
      'upload': 'open_uploader'
      'albums': 'open_albums_editor'

    open_uploader: ->
      $('#photo-manager').trigger('open_uploader')

    open_albums_editor: ->
      $('#photo-manager').trigger('open_albums_editor')
