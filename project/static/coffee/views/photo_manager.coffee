class PhotoManager extends Backbone.View
  el: '#photo-manager'

  events:
    'open_uploader': 'open_uploader'
    'open_albums_editor': 'open_albums_editor'
    'open_photos_editor': 'open_photos_editor'
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
    @$('nav a').removeClass('selected')
    @$('nav .upload').addClass('selected')
    @albums_editor.close()
    @photo_feed.close_photos_info()
    @uploader.$el.addClass('open')

  open_albums_editor: ->
    @$('nav a').removeClass('selected')
    @$('nav .edit-albums').addClass('selected')
    @uploader.close()
    @photo_feed.close_photos_info()
    @albums_editor.$el.addClass('open')

  open_photos_editor: ->
    @$('nav a').removeClass('selected')
    @$('nav .edit-photos').addClass('selected')
    @uploader.close()
    @albums_editor.close()
    @photo_feed.open_photos_info()

  add_photos_to_album: (event) ->
    album_id = $(event.currentTarget).data('id')
    album = @user_albums.get(album_id)
    _.each @photo_feed.selected_photos(), (model) ->
      photos = album.get('photos') or []
      photos.push model
      album.set('photos', photos)
    album.save()
    text = "The selected photos have been added to #{album.get('title')}."
    Notification.show(text)
    @photo_feed.clear_selections()

  add_tags: ->
    input_value = @$('.bulk-editor input').val()
    tags = input_value.split(',')
    _.each @photo_feed.selected_photos(), (photo) ->
      photo_tags = _.union(photo.get('public_tags'), tags)
      photo.set('public_tags', photo_tags)
      text = "Added tags #{input_value} to selected photos."
      photo.save {}, success: -> Notification.show(text)
    @$('.bulk-editor').removeClass('open')

  open_bulk_editor: ->
    @$('.bulk-editor input').val('')
    @$('.bulk-editor').addClass('open')
