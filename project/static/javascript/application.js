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

var AppView = Backbone.View.extend({
  initialize: function () {
    new Uploader()
  }
});

jQuery('document').ready(function () {
  var App = new AppView()
});
