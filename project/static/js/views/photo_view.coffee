define [
  'cs!views/photo_image'
  'cs!views/photo_info'
], (PhotoImage, PhotoInfo) ->
  class PhotoView extends Backbone.View
    className: 'photo'

    events:
      'click': 'goto_photo_page'

    initialize: ->
      @$el.data('href', "/photos/#{@model.get('id')}")
      img = new PhotoImage({@model})
      @$el.append(img.$el)
      info = new PhotoInfo({@model})
      @$el.append(info.$el)

    set_height: (height) ->
      @$el.height(height)
      @$el.width(@model.width_from(height))

    set_width: (width) ->
      @$el.width(width)
      @$el.height(@model.height_from(width))

    goto_photo_page: ->
      window.location = @$el.data('href')
