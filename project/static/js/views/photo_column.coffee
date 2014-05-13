define [], ->
  class PhotoColumn extends Backbone.View
    className: 'column'

    set_width: (width) ->
      # TODO Get the margin widths before appending to photo feed
      margin_widths = 4
      @width = width - margin_widths
      @$el.width(@width)

    get_width: -> @width

    append: (view) -> @$el.append(view.$el)
