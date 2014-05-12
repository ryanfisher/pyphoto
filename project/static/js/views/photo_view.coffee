define ['cs!views/photo_image'], (PhotoImage) ->
  class PhotoView extends Backbone.View
    tagName: 'a'
    className: 'photo'

    initialize: ->
      @$el.attr('href', "/photos/#{@model.get('id')}")
      img = new PhotoImage({@model})
      @$el.append(img.$el)

    set_height: (height) ->
      @$el.height(height)
      @$el.width(@model.width_from(height))

    set_width: (width) ->
      @$el.width(width)
      @$el.height(@model.height_from(width))
