const search = document.getElementById('search');
const showsOrder = document.getElementById('shows-order');
const showsQuantity = document.getElementById('shows-quantity');
const showsAscDesc = document.getElementById('shows-asc-desc');
const showMovies = document.getElementById('showMovies')

search.addEventListener('input', async function(){
    await fetchShows();
});
showsOrder.addEventListener('change', async function(){
    await fetchShows();
})
showsQuantity.addEventListener('change', async function(){
    await fetchShows();
})
showsAscDesc.addEventListener('change', async function(){
    await fetchShows();
})

async function fetchShows(){
    let response = await fetch('/search?q=' + search.value + "&shows-order=" + showsOrder.value + "&shows-quantity=" + showsQuantity.value + "&shows-asc-desc=" + showsAscDesc.value);
    console.log(response);
    let shows = await response.json();
    let html = "";
    for (let id in shows) {
        let title = shows[id].title;
        html += '<li>' + title + '</li>';
    }
    showMovies.innerHTML = html;
}