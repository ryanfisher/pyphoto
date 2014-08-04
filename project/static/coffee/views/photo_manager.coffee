class PhotoManager extends Backbone.View
  el: '#photo-manager'

  events:
    'open_uploader': 'open_uploader'
    'open_albums_editor': 'open_albums_editor'
    'click .add-to-albums li': 'add_photos_to_album'
    'click .add-tags': 'open_bulk_editor'
    'click .bulk-editor button': 'add_tags'

  initialize: ->
    @uploader = new Uploader({@collection})
    collection = new UserAlbums
    no_albums_notice = @$('.no-albums-notice')
    album_dropdown = @$('.add-to-albums .inner-dropdown')
    collection.on 'add', (model) ->
      no_albums_notice.remove()
      set_up_album = ->
        li = $('<li>', data: {id: model.get('id')}, text: model.get('title'))
        model.on 'destroy', -> li.remove()
        album_dropdown.append(li)
      if model.get('id')
        set_up_album()
      else
        model.on 'change:id', set_up_album
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
    album_id = $(event.currentTarget).data('id')
    album = @user_albums.get(album_id)
    _.each @photo_feed.selected_photos(), (view) ->
      photos = album.get('photos') or []
      photos.push view.model
      album.set('photos', photos)
    album.save()
    (new Notification).show(
      "The selected photos have been added to #{album.get('title')}."
    )
    @photo_feed.clear_selections()

  add_tags: ->
    tags = @$('.bulk-editor input').val().split(',')
    _.each @photo_feed.selected_photos(), (view) ->
      photo = view.model
      photo_tags = _.union(photo.get('public_tags'), tags)
      photo.set('public_tags', photo_tags)
      photo.save()
    @$('.bulk-editor').removeClass('open')

  open_bulk_editor: ->
    @$('.bulk-editor').addClass('open')
