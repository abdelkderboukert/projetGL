window.addEventListener('resize', function() {
    var containerWidth = document.getElementById('contt').offsetWidth;
    var textElement = document.getElementById('titre');
    textElement.style.fontSize = (containerWidth / 25) + 'px';
  });
  
  // Initial font size
  var containerWidth = document.getElementById('contt').offsetWidth;
  var textElement = document.getElementById('titre');
  textElement.style.fontSize = (containerWidth / 25) + 'px';