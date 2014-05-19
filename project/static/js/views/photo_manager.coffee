define [
  'cs!views/manager/albums_editor'
  'cs!views/manager/photo_feed'
  'cs!collections/user_albums'
  'cs!views/manager/uploader'
], (AlbumsEditor, PhotoManagerFeed, UserAlbums, Uploader) ->
  class PhotoManager extends Backbone.View
    el: '#photo-manager'

    events:
      'open_uploader': 'open_uploader'
      'open_albums_editor': 'open_albums_editor'
      'change #album-dropdown': 'add_photos_to_album'

    initialize: ->
      @uploader = new Uploader({@collection})
      collection = new UserAlbums
      collection.on 'add', (model) ->
        select = $('<option>', val: model.get('id'), text: model.get('title'))
        $('#album-dropdown').append(select)
      @user_albums = collection
      @albums_editor = new AlbumsEditor({collection})
      @photo_feed = new PhotoManagerFeed({@collection})

    open_uploader: ->
      @albums_editor.close()
      @uploader.$el.addClass('open')

    open_albums_editor: ->
      @uploader.close()
      @albums_editor.$el.addClass('open')

    add_photos_to_album: (event) ->
      option = $(event.target).find('option:selected')
      $('#album-dropdown')[0].selectedIndex = 0
      album = @user_albums.get(option.val())
      _.each @photo_feed.selected_photos(), (view) ->
        photos = album.get('photos') or []
        photos.push view.model
        album.set('photos', photos)
      album.save()
