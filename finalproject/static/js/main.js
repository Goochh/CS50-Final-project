
const searchInput = document.getElementById('search-input');
const cards = document.getElementsByClassName('card');

searchInput.addEventListener('input', (e) => {
  const searchValue = e.target.value.toLowerCase();
  
  for (let card of cards) {
    const cardTitle = card.getElementsByClassName('card-title')[0].textContent.toLowerCase();
    if (cardTitle.includes(searchValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  }
});