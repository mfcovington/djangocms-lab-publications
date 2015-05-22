// Based on: http://stackoverflow.com/a/9204307/996114
function containsAll(query, target) {
    var success;

    if (query === null) {
      success = true;
    }
    else{
      success = $.grep(query, function(n, i) {
          return $.inArray(n, target) !== -1;
      }).length === query.length;
    };

    return success;
}

function filterByTags(list) {
  pubList.filter(function(item) {
    var query = $( ".pub-tags-select" ).val();
    var pub_tags = item.values().tags.trim().split(/\s+/);
    if (containsAll(query, pub_tags)) {
      return true;
    } else {
      return false;
    }
  });
}

$( ".pub-tags-select" ).change(function() {
  filterByTags(pubList);
});

$( "#pub-search" ).keyup(function() {
  filterByTags(pubList);
});

$(".pub-tags-select").select2({
    placeholder: "Filter Keywords",
});

// Make Filter Combo box style more consistent with Search box
// These get overridden by select2.min.css is set in app.css
$('.select2-search__field').css({
  'margin-top': '6px',
  'padding': '0',
});
$('.select2-selection__rendered').css('padding', '0 12px');
