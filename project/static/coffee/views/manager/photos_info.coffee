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

  set_info: (photos) ->
    tags = _.invoke photos, 'get', 'public_tags'
    common_tags = _.intersection tags...
    @$('.tags').text common_tags
    @set_photo(photos[0])

  unset_info: ->
    @$('.tags').text ''
    @unset_photo()

  update: (photos) ->
    if photos.length > 0
      @set_info photos
    else
      @unset_info()
