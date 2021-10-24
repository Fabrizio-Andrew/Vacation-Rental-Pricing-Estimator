document.addEventListener('DOMContentLoaded', () => {

    // Get all "sidebar-item" elements
    const $sidebarButtons = Array.prototype.slice.call(document.querySelectorAll('.sidebar-item'), 0);
  
    // Check if there are any navbar burgers
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
  
  });