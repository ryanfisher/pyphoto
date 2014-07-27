class PhotoFeed extends Backbone.View
  el: '#photo-feed'

  PHOTO_HEIGHT = 250
  PHOTO_WIDTH_MIN = 300
  USE_COLUMNS = true

  initialize: ->
    @render()
    @window_width = $(window).width()
    $(window).on 'resize', =>
      width = $(window).width()
      # We only need to reset the photo feed when window width changes
      return if width == @window_width
      @window_width = width
      @render()

  render: ->
    # We set the scrollbar here so the width doesn't change when photos
    # overflow from view and scroll is automatically added
    $('html').css('overflow-y', 'scroll')
    @set_up_columns() if USE_COLUMNS
    @collection.each (model) =>
      photo_view = new PhotoView({model})
      if USE_COLUMNS
        photo_view.set_width(@columns[0].get_width())
        column = _.min @columns, (col) -> col.height
        column.append(photo_view)
      else
        photo_view.set_height(PHOTO_HEIGHT)
        @$el.append(photo_view.$el)

  set_up_columns: ->
    @$el.text('')
    column_count = Math.floor(@$el.width() / PHOTO_WIDTH_MIN)
    width = @$el.width() / column_count
    @columns = (new PhotoColumn for i in [1..column_count])
    @$el.append(col.set_width(width).$el) for col in @columns
