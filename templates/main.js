window.addEventListener('load', function() {
    const toggleSwitch = document.querySelector('#toggle-dark-theme');
    const toggleSwitchLabel = document.querySelector('#toggle-dark-theme-label');
  
    function switchTheme(event) {
      if (event.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
      }
    }
  
    toggleSwitch.addEventListener('change', switchTheme, false);
  
    // Check local storage for saved theme and set as default
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
      document.documentElement.setAttribute('data-theme', currentTheme);
      if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
      }
    }
  
    // Update label based on theme preference
    toggleSwitchLabel.textContent = `Toggle ${currentTheme === 'dark' ? 'light' : 'dark'} theme`;
  });
  
  function startCountdown() {
    var seconds = 60;
    var countdownElement = document.getElementById("countdown");
    var countdownInterval = setInterval(function() {
      countdownElement.innerHTML = "<span id='countdown-title'>Time left: </span>" + seconds;
      seconds -= 1;
      if (seconds < 0) {
        clearInterval(countdownInterval);
        location.reload();
      }
    }, 1000);
  }
  
  startCountdown();
  
  // Set default theme to afternoon if current time is between 12 and 18
  let currentHour = new Date().getHours();
  if (currentHour >= 12 && currentHour < 18) {
    document.body.setAttribute("data-theme", "afternoon");
  }
  
  var date = new Date();
  var hour = date.getHours();
  
  if (hour >= 12 && hour < 18) {
    document.documentElement.setAttribute("data-theme", "afternoon");
  } else if (hour >= 18 || hour < 6) {
    document.documentElement.setAttribute("data-theme", "dark");
  } else {
    document.documentElement.setAttribute("data-theme", "morning");
  }
  
  // Add event listener to radio buttons
  const radios = document.querySelectorAll('input[type="radio"]');
  radios.forEach(radio => {
    radio.addEventListener('change', event => {
      localStorage.setItem('theme', event.target.value);
    });
  });
  
  // Get the selected theme from localStorage (if it exists)
  const storedTheme = localStorage.getItem('theme');
  
  // Set the initial theme based on the stored theme or default to "dark"
  let currentTheme = storedTheme || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);
  
  // Listen for changes to the radio buttons and update the theme accordingly
  const radioButtons = document.querySelectorAll('input[name="theme"]');
  radioButtons.forEach((button) => {
    button.addEventListener('change', (event) => {
      currentTheme = event.target.value;
      document.documentElement.setAttribute('data-theme', currentTheme);
      localStorage.setItem('theme', currentTheme);
    });
  });
  