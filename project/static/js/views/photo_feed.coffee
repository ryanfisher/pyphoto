define [
  'cs!views/photo_column'
  'cs!views/photo_view'
], (PhotoColumn, PhotoView) ->
  class PhotoFeed extends Backbone.View
    el: '#photo-feed'

    PHOTO_HEIGHT = 250
    USE_COLUMNS = true

    initialize: ->
      @set_up_columns() if USE_COLUMNS
      @collection.on 'add', (model) =>
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
      @current_col = 0
      column_count = 4
      width = @$el.width() / column_count
      @columns = []
      for i in [1..column_count]
        col = new PhotoColumn
        col.set_width(width)
        @columns.push(col)
        @$el.append(col.$el)
