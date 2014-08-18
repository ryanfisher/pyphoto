class PhotosInfo extends Backbone.View
  el: '#photos-info'

  set_photo: (model) ->
    @$('img').prop('src', model.get('thumbnail_url'))

  unset_photo: ->
    @$('img').prop('src', '')

  open: ->
    @$el.addClass('open')

  close: ->
    @$el.removeClass('open')

  update: (photos) ->
    count = photos.length
    if count == 1
      @set_photo(photos[0])
    else
      @unset_photo()
