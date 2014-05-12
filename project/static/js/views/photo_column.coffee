define [], ->
  class PhotoColumn extends Backbone.View
    className: 'column'

    set_width: (width) ->
      @$el.width(width)
      @width = width

    get_width: -> @width

    append: (view) -> @$el.append(view.$el)
