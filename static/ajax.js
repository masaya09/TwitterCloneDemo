const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const handleClicked = async (e) => {
  e.preventDefault();

  const likeButton = e.currentTarget;
  const url = likeButton.dataset.url;

  const data = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  };

  const response = await fetch(url, data);
  const jsonResponse = await response.json();

  handleChangeStyle(jsonResponse, likeButton, url)
};

const handleChangeStyle = (response, likeButton, url) => {
  const split_url = url.split("/");
  const count = document.querySelector(`[name="count_${response.tweet_id}"]`)

  if(response.is_liked) {
    unlike_url = url.replace(split_url[3], "unlike");
    likeButton.setAttribute("data-url", unlike_url);
    likeButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" id="heart" class="h-4 w-4 cursor-pointer text-pink-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" /></svg>`;
    count.innerHTML = response.likes_count;
  } else {
    like_url = url.replace(split_url[3], "like");
    likeButton.setAttribute("data-url", like_url);
    likeButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" id="blank-heart" class="h-4 w-4 cursor-pointer hover:text-pink-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>';
    count.innerHTML = response.likes_count;
  }
};

const likedList = [...document.querySelectorAll("[data-button='like']")];

likedList.map(liked => {
  liked.addEventListener("click", handleClicked);
})
