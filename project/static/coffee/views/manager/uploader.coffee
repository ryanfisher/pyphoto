class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'click h4': 'toggle_open'
    'change input': 'upload_photos'

  initialize: ->
    $('#id_file').hide()
    @uploading = false

  close: ->
    @$el.removeClass('open')

  toggle_open: ->
    @$('form').toggleClass('hidden')

  upload_photos: ->
    return if @uploading
    @uploading = true
    for photo_file in @$('.multiple-photos')[0].files
      info = new ProgressInfo(photo_file)
      @send_request(photo_file, info)

  send_request: (photo_file, progress_info)->
    info = progress_info
    form_data = new FormData()
    form_data.append('file', photo_file)
    csrf_token = @$('input[name="csrfmiddlewaretoken"]').val()
    $.ajax
      type: "POST"
      url: "/api/photos"
      data: form_data
      headers: 'X-CSRFToken': csrf_token
      success: (data) =>
        @collection.add data
        info.display_message(200)
      error: (jqXHR) -> info.display_message(jqXHR.status)
      complete: =>
        info.stop_animation()
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
              info.update_bar(percentUploaded)
          myXhr.upload.addEventListener 'progress', callback, false
        myXhr
