from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="bnhhddqlrbvomu6cn7l9749bo0",
    auth_token="MF8FUGIrVlevM7VpU9WkYLADOJtG3hHIXlCt%2BAedI98qY52KtDtKr3RJDsoe6OeZ%2FLXbYTaQgdsSqiyifCNdjw%3D%3D",
    host="https://gogoanime.pe/"  
)

def download(search = 'chainsaw-man', quality="link_720p"):
    details = anime.get_details(animeid=search)
    episodes = details.episodes
    for i in range(1, episodes+1):
        anime_link = anime.get_episode_link_advanced(animeid=search , episode_num=i)
        print(anime_link)

download()