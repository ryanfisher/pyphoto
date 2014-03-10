var Uploader = Backbone.View.extend({
  el: "#uploader",

  events: {
    'click input[type="submit"]': "upload_photo",
  },

  initialize: function () {
    console.log("Uploader initialized")
  },

  upload_photo: function () {
    event.preventDefault();
  }
});

jQuery('document').ready(function() {
  new Uploader();
});
