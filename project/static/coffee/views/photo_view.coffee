class PhotoView extends Backbone.View
  className: 'photo'

  events:
    'click': 'goto_photo_page'

  initialize: ->
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
    window.location = "/photos/#{@model.get('id')}"
