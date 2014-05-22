define [
  'cs!views/manager/photo_edit_view'
  'cs!models/user_photo'
], (PhotoEditView, UserPhoto) ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'click .close-button': 'close'
      'click .save-album': 'save'

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
      @model.get('photos').each (model) ->
        view = new PhotoEditView({model})
        view.$el.data('id', model.get('id'))
        @$('.photos').append view.$el

    set_cover: ->
      @$('.cover-photo').css(
        'background-image'
        @$('.photo').css('background-image')
      )

    close: ->
      @undelegateEvents()
      @$el.removeClass('open')

    save: ->
      photos = @model.get('photos')
      @$('.photos .photo').each (index) ->
        photo = photos.get($(this).data('id'))
        photo.set('position', index + 1)
      @model.save()
