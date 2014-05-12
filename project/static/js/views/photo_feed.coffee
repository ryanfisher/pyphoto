define [], ->
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
      width = $(window).width() / column_count
      @columns = []
      for i in [1..column_count]
        col = new PhotoColumn
        col.set_width(width-8)
        @columns.push(col)
        @$el.append(col.$el)

  class PhotoColumn extends Backbone.View
    className: 'column'

    set_width: (width) ->
      console.log width
      @$el.width(width)
      @width = width

    get_width: -> @width

    append: (view) -> @$el.append(view.$el)

  class PhotoImg extends Backbone.View
    tagName: 'img'
    className: 'hidden'

    initialize: ->
      @$el.on 'load', => @$el.removeClass('hidden')
      @$el.attr('src', @model.get('thumbnail_url'))

  class PhotoView extends Backbone.View
    tagName: 'a'
    className: 'photo'

    initialize: ->
      @$el.attr('href', "/photos/#{@model.get('id')}")
      img = new PhotoImg({@model})
      @$el.append(img.$el)

    set_height: (height) ->
      @$el.height(height)
      @$el.width(@model.width_from(height))

    set_width: (width) ->
      @$el.width(width)
      @$el.height(@model.height_from(width))

  PhotoFeed
