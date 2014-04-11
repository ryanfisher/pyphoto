
class PhotoManagerEditView extends Backbone.View
  className: 'photo'

  initialize: ->
    thumbnail_url = "url(#{@model.get('thumbnail_url')})".replace /\s/, "%20"
    @$el.css('background-image', thumbnail_url)

class PhotoManagerFeed extends Backbone.View
  el: '#photo-manager-feed'

  initialize: ->
    @collection.on 'add', (model) =>
      photo_edit_view = new PhotoManagerEditView({model})
      @$el.append(photo_edit_view.$el)

class PhotoFeed extends Backbone.View
  el: '#photo-feed'

  initialize: ->
    @collection.on 'add', (model) =>
      photo_view = new PhotoView({model})
      @$el.append(photo_view.$el)

class PhotoImg extends Backbone.View
  tagName: 'img'

  initialize: ->
    @$el.attr('src', @model.get('thumbnail_url'))

class PhotoView extends Backbone.View
    tagName: 'a'
    className: 'photo'

    initialize: ->
      @$el.attr('href', "/photos/#{@model.get('id')}")
      img = new PhotoImg({@model})
      @$el.append(img.$el)

class UserPhoto extends Backbone.Model

class UserPhotos extends Backbone.Collection
  url: '/api/photos'
  model: UserPhoto

class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'submit form' : "upload_photos"

  initialize: ->
    $('#id_file').hide()
    @uploading = false

  send_request: (photo_file, progress_info)->
    info = progress_info
    form_data = new FormData()
    form_data.append('file', photo_file)
    csrf_token = @$('input[name="csrfmiddlewaretoken"]').val()
    $.ajax
      type: "POST"
      url: "/upload"
      data: form_data
      headers: 'X-CSRFToken': csrf_token
      success: (data) -> info.find('.success').show()
      error: (jqXHR) ->
        if jqXHR.status == 409
          info.find('.error409').show()
        else
          info.find('.failure').show()
      complete: =>
        info.find('.bar').removeClass('animated')
        @uploading = false;
        @$('form')[0].reset();
      processData: false,
      contentType: false,
      xhr: ->
        myXhr = $.ajaxSettings.xhr();
        if myXhr.upload
          callback = (ev) ->
            if ev.lengthComputable
              percentUploaded = Math.floor(ev.loaded * 100 / ev.total)
              console.info('Uploaded '+percentUploaded+'%')
              info.find('.bar').css('width', percentUploaded+'%')
            else
              console.info('Uploaded '+ev.loaded+' bytes')
          myXhr.upload.addEventListener 'progress', callback, false
        myXhr

  upload_photos: ->
    event.preventDefault()
    return if @uploading
    @uploading = true
    form = $(event.target)
    file_input = form.find('[type="file"]:visible')
    for photo_file in file_input[0].files
      info = @$('.progress-info').first().clone()
      @$el.append(info)
      @send_request(photo_file, info)

class AppView extends Backbone.View

  initialize: ->
    new Uploader()
    collection = new UserPhotos
    new PhotoFeed({collection})
    new PhotoManagerFeed({collection})
    collection.fetch()

jQuery('document').ready ->
  App = new AppView()
