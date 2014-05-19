define [
  'cs!views/manager/photo_edit_view'
  'cs!models/user_photo'
], (PhotoEditView, UserPhoto) ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'click .close-button': 'close'

    initialize: ->
      @$('.title').text @model.get('title')
      @set_photos()
      @$el.addClass('open')
      @$('.photos').sortable(
        scroll: false
        placeholder: 'sortable-placeholder'
        cursor: 'move'
      )

    set_photos: ->
      @$('.photos').text ''
      for photo in @model.get('photos')
        model = new UserPhoto(photo)
        view = new PhotoEditView({model})
        @$('.photos').append view.$el

    close: ->
      @$el.removeClass('open')
