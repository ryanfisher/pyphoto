class AlbumEditor extends Backbone.View
  el: '#album-editor'

  events:
    'click .close-button': 'close'
    'click .save-album': 'save'
    'click .remove-selected': 'remove_selected'
    'click .delete-album': 'delete_album'

  initialize: ->
    @$('.title').text @model.get('title')
    @set_photos()
    @set_cover()
    @$el.addClass('open')
    @$('.photos').sortable(
      scroll: false
      placeholder: 'sortable-placeholder'
      cursor: 'move'
      stop: => @set_cover()
    )

  set_photos: ->
    @$('.photos').text ''
    @model.get('photos').each (model) =>
      view = new PhotoEditView({model})
      view.$el.data('id', model.get('id'))
      @$('.photos').append view.$el

  set_cover: ->
    @$('.cover-photo').css(
      'background-image'
      @$('.photo').css('background-image')
    )

  remove_selected: ->
    selected_photos = @$('.photo.selected')
    photos_in_album = @model.get('photos')
    ids_to_remove = ($(photo).data('id') for photo in selected_photos)
    photos_to_remove = (photos_in_album.get(id) for id in ids_to_remove)
    selected_photos.remove()
    photos_in_album.remove(photos_to_remove)

  delete_album: ->
    confirm_text = 'Are you sure you want to delete this album?'
    return unless window.confirm(confirm_text)
    @model.destroy()
    @close()

  close: ->
    @$('.cover-photo').css('background-image', 'none')
    @undelegateEvents()
    @$el.removeClass('open')

  save: ->
    photos = @model.get('photos')
    @$('.photos .photo').each (index) ->
      photo = photos.get($(this).data('id'))
      photo.set('position', index + 1)
    @model.save {}, success: -> Notification.show('Album saved successfully!')
