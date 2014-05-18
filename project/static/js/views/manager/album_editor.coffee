define [
  'cs!views/manager/photo_edit_view'
  'cs!models/user_photo'
], (PhotoEditView, UserPhoto) ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'click .close-button': 'close_editor'
      'dragstart .photo': 'dragging'
      'dragover .photo': 'dragover_issue'
      'drop .photo': 'drop_photo'

    initialize: ->
      @$('.title').text @model.get('title')
      @set_photos()
      @$el.addClass('open')

    dragover_issue: (event) ->
      # This is necessary to make drag and drop work for some reason
      event.preventDefault()
      event.stopPropagation()

    set_photos: ->
      @$('.photos').text ''
      for photo in @model.get('photos')
        model = new UserPhoto(photo)
        view = new PhotoEditView({model})
        @$('.photos').append view.$el

    close_editor: ->
      @$el.removeClass('open')

    dragging: (event) ->
      @dragging_photo = $(event.target)

    drop_photo: (event) ->
      # TODO update album photo positions
      $(event.target).after(@dragging_photo)
