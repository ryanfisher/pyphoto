class PhotoManagerFeed extends Backbone.View
  el: '#photo-manager-feed'

  events:
    'click .feed-container': 'clear_selections'
    'click .delete-link':    'delete_photos'
    'click .sort-by li':     'sort_by'

  initialize: ->
    @render()

  sort_by: (event) ->
    @$('.sort-by li').removeClass('selected')
    sort_type = $(event.currentTarget).addClass('selected').data('sort-type')
    @collection.sort_by(sort_type)
    @reset()
    @update_selected_count()

  reset: ->
    @photo_edit_views = []
    @$('.feed').empty()
    @collection.each (model) =>
      @new_photo_view model
      @$('.feed').append @last_photo_view_el()

  render: ->
    @photo_edit_views = []
    @collection.on 'add', (model) =>
      @new_photo_view model
      @$('.feed').append @last_photo_view_el()
    @collection.once 'sync', =>
      @collection.off 'add'
      @collection.on 'add', (model) =>
        @new_photo_view model
        @$('.feed').prepend @last_photo_view_el()

  new_photo_view: (model) ->
    photo_edit_view = new PhotoEditView({model})
    photo_edit_view.on 'selected_toggle', => @update_selected_count()
    @photo_edit_views.push photo_edit_view

  last_photo_view_el: ->
    @photo_edit_views[@photo_edit_views.length - 1].$el

  delete_photos: ->
    @delete_selected_photos()
    @update_selected_count()

  clear_selections: (event) ->
    target = $(event?.target)
    return unless target.attr('class')?.match(/feed|feed-container/)
    @$('.feed .selected').removeClass('selected')
    @update_selected_count()

  update_selected_count: ->
    selected_count = @$('.feed .selected').length
    if selected_count > 0
      @$('.photos-selected').removeClass('hidden')
    else
      @$('.photos-selected').addClass('hidden')
      @$('.bulk-editor').removeClass('open')
    @$('.selected-count').text selected_count

  # A list of photo views currently selected in the photo manager feed
  #
  # @todo I might want to make this return the models of those views instead
  #
  # @return [Array<PhotoEditView>]
  selected_photos: ->
    _.filter @photo_edit_views, (view) -> view.is_selected()

  delete_selected_photos: ->
    to_delete = @selected_photos()
    delete_count = to_delete.length
    return if delete_count == 0
    confirm_text = "Are you sure you want to delete the selected photo(s)?" +
                   "\n\n#{delete_count} selected"
    if window.confirm(confirm_text)
      _.each to_delete, (view) -> view.delete_photo()
