function AddLike(likesCount) {
    countLikes = document.getElementById(`likes_${likesCount}`)
    count = Number(countLikes.textContent)
    like = document.getElementById(`like_${likesCount}`)

    dislike = document.getElementById(`dislike_${likesCount}`)
    countDislikes = document.getElementById(`dislikes_${likesCount}`)
    counts = Number(countDislikes.textContent)
    if (like.style.background == 'blue') {
        like.style.background = ""
        like.style.color = ""
        countLikes.innerHTML = + count - 1
    } else {
        like.style.background = "blue"
        like.style.color = "white"
        dislike.style.background = ""
        dislike.style.color = ""
        countLikes.innerHTML = count + 1
        if (countDislikes.textContent == 0) {
            countDislikes.innerHTML = counts
        } else {
            countDislikes.innerHTML = + counts - 1
        }
    }
}

function AddDislike(dislikeCount) {
    countDislikes = document.getElementById(`dislikes_${dislikeCount}`)
    count = Number(countDislikes.textContent)
    dislike = document.getElementById(`dislike_${dislikeCount}`)

    like = document.getElementById(`like_${dislikeCount}`)

    countLikes = document.getElementById(`likes_${dislikeCount}`)
    counts = Number(countLikes.textContent)
    if (dislike.style.background == 'red') {
        dislike.style.background = ""
        dislike.style.color = ""
        countDislikes.innerHTML = + count - 1
    } else {
        dislike.style.background = "red"
        dislike.style.color = "white"
        like.style.background = ""
        like.style.color = ""
        countDislikes.innerHTML = + 1
        if (countLikes.textContent == 0) {
            countLikes.innerHTML = counts
        } else {
            countLikes.innerHTML = counts - 1
        }
    }
}