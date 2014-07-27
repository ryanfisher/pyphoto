class PhotoColumn extends Backbone.View
  className: 'column'

  initialize: ->
    @height = 0

  set_width: (width) ->
    # TODO Get the margin widths before appending to photo feed
    margin_widths = 4
    @width = width - margin_widths
    @$el.width(@width)
    this

  get_width: -> @width

  append: (view) ->
    @height += view.$el.height()
    @$el.append(view.$el)
