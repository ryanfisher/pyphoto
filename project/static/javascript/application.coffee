
class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'submit form' : "upload_photos"

  initialize: ->
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
    info = @$('.progress-info').first().clone()
    @$el.append(info)
    @uploading = true
    form = $(event.target)
    file_input = form.find('#id_file')
    photo_file = file_input[0].files[0]
    @send_request(photo_file, info)

class AppView extends Backbone.View

  initialize: -> new Uploader()

jQuery('document').ready ->
  App = new AppView()
