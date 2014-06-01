define [
  'cs!views/photo_column'
  'cs!views/photo_view'
], (PhotoColumn, PhotoView) ->
  class PhotoFeed extends Backbone.View
    el: '#photo-feed'

    PHOTO_HEIGHT = 250
    PHOTO_WIDTH_MIN = 300
    USE_COLUMNS = true

    initialize: ->
      @render()
      $(window).on 'resize', => @render()

    render: ->
      @set_up_columns() if USE_COLUMNS
      @collection.each (model) =>
        photo_view = new PhotoView({model})
        if USE_COLUMNS
          photo_view.set_width(@columns[0].get_width())
          @columns[@current_col].append(photo_view)
          @current_col++
          @current_col = 0 if @current_col == @columns.length
        else
          photo_view.set_height(PHOTO_HEIGHT)
          @$el.append(photo_view.$el)

    set_up_columns: ->
      @$el.text('')
      @current_col = 0
      column_count = Math.floor(@$el.width() / PHOTO_WIDTH_MIN)
      width = @$el.width() / column_count
      @columns = (new PhotoColumn for i in [1..column_count])
      @$el.append(col.set_width(width).$el) for col in @columns
