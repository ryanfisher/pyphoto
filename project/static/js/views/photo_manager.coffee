define [
  'cs!views/manager/album_editor'
  'cs!views/manager/photo_feed'
  'cs!collections/user_albums'
  'cs!views/manager/uploader'
], (AlbumEditor, PhotoManagerFeed, UserAlbums, Uploader) ->
  class PhotoManager extends Backbone.View
    el: '#photo-manager'

    events:
      'open_uploader': 'open_uploader'
      'open_album_editor': 'open_album_editor'

    initialize: ->
      @uploader = new Uploader({@collection})
      collection = new UserAlbums
      collection.on 'add', (model) ->
        select = $('<option>', val: model.get('id'), text: model.get('title'))
        $('#album-dropdown').append(select)
      @album_editor = new AlbumEditor({collection})
      @photo_feed = new PhotoManagerFeed({@collection})

    open_uploader: ->
      @album_editor.$el.removeClass('open')
      @uploader.$el.addClass('open')

    open_album_editor: ->
      @uploader.$el.removeClass('open')
      @album_editor.$el.addClass('open')
