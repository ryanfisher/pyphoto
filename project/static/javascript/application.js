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
        alert('Done Uploading');
      },
      processData: false,
      contentType: false
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
