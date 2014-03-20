var Uploader = Backbone.View.extend({
  el: "#uploader",

  events: {
    'submit form': "upload_photo",
  },

  initialize: function () {
    console.log("Uploader initialized")
    this.uploading = false
  },

  upload_photo: function () {
    event.preventDefault();
    if (this.uploading) {
      console.log("currently uploading");
      return;
    };
    this.uploading = true;
    form = $(event.target);
    file_input = form.find('#id_file');
    photo_file = file_input[0].files[0];
    form_data = new FormData();
    form_data.append('file', photo_file)
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
    _this = this;
    $.ajax({
      type: "POST",
      url: "/upload",
      data: form_data,
      headers: { 'X-CSRFToken': csrf_token },
      success: function (data) {
        _this.uploading = false;
        form[0].reset();
      },
      processData: false,
      contentType: false,
      xhr: function() {
        var myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
            myXhr.upload.addEventListener('progress',function(ev) {
                if (ev.lengthComputable) {
                    var percentUploaded = Math.floor(ev.loaded * 100 / ev.total);
                    console.info('Uploaded '+percentUploaded+'%');
                    // update UI to reflect percentUploaded
                } else {
                    console.info('Uploaded '+ev.loaded+' bytes');
                    // update UI to reflect bytes uploaded
                }
           }, false);
        }
        return myXhr;
      }
    });
  }
});

var AppView = Backbone.View.extend({
  initialize: function () {
    new Uploader()
  }
});

jQuery('document').ready(function () {
  var App = new AppView()
});
