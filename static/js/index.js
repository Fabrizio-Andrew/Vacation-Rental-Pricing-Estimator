document.addEventListener('DOMContentLoaded', () => {

  // Get all "sidebar-item" elements
  const $sidebarButtons = Array.prototype.slice.call(document.querySelectorAll('.sidebar-item'), 0);

  // Check if there are any sidebar buttons
  if ($sidebarButtons.length > 0) {

    // Add a click event on each of them
    $sidebarButtons.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle "sidebar-active" class on the "sidebar-item" and "form-active" on the secondary bar
        if (el.classList.contains('sidebar-active')) {
            el.classList.remove('sidebar-active');
        } else {
          $sidebarButtons.forEach (button => {
              button.classList.remove('sidebar-active');
          });
          el.classList.toggle('sidebar-active');
        }
        $target.classList.toggle('form-active');
        $target.style.display = 'block';
        $target.style.animationPlayState ='running';
      });
    });
  }

  document.querySelector('#submit').onclick = () => submitForm();

});

function submitForm() {
  fetch('/estimate', {
    method: 'POST',
    body: JSON.stringify({
      'host_resp': document.querySelector('#response_time').value,
      'dist_to_landmark': document.querySelector('#dist_to_landmark').value,
      'longitude': document.querySelector('#long').value,
      'latitude': document.querySelector('#lat').value,
      'room_type': document.querySelector('#room_type').value,
      'review_scores_rating': document.querySelector('#review_score').value,
      'beds': document.querySelector('#beds').value,
      'accommodates': document.querySelector('#accomodates').value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)

    // plug response values into the dashboard
    document.querySelector('#estimate-figure').innerHTML = `$${result.estimate}`;
    document.querySelector('#percentile-figure').innerHTML = `${result.percentile}%`;

    // Clear content from the opportunities box.
    var opportunities = document.querySelector('#opportunities-box');
    opportunities.innerHTML = '';

    // If recommendations, then show opportunities box with all of them
    if (result.recommendations.length > 0) {

      // Create a content div
      var oppcontent = document.createElement('div');
      oppcontent.className = 'content is-medium';
      
      // Add the title
      var title = document.createElement('h2');
      title.innerHTML = 'Opportunities:'
      var br = document.createElement('br');
      oppcontent.append(title);

      // Create recommendations list
      var recul = document.createElement('ul');

      for (i=0; i < result.recommendations.length; i++) {
        recli = document.createElement('li');
        recli.innerHTML = generateRecommendation(result.recommendations[i]);
        recul.append(recli);
      }
      oppcontent.append(recul);
      opportunities.append(oppcontent);
      opportunities.style.display = 'block';

    } else {
      document.querySelector('#opportunities-box').style.display = 'none';
    }

    // Hide placeholder content and display dashboard
    document.querySelector('#placeholder-content').style.display = 'none';
    document.querySelector('#dashboard').style.display = 'flex';

    // Remove "active" styling from button and slide out form
    sidebutton = document.querySelector('#estimator-form-button');
    sidebutton.classList.remove('sidebar-active');

    const targ = document.querySelector('#submit').dataset.target;
    const $targ = document.getElementById(targ);
    $targ.classList.toggle('form-active');

  })
}

function generateRecommendation(recabbrev) {
  switch (recabbrev) {
    case 'response_time':
      var result = 'Hosts who take too long to respond to customer inquiries tend to command a lower rate.  Shortening your response time may ultimate help improve your revenue.';
      break;
    case 'landmark':
      var result = 'Your rental property is located closer than average to a major attraction.  Be sure to highlight your proximity to attractions to improve booking rates and command the best price.';
      break;
  }
  return result;
}