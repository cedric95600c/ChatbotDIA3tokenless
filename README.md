# Song-Recommander
A little song recommander in python (a noter que ce code n'est pas fonctionnel en local, car il faut un token d'accès fournit dans le .zip pour lancer le serveur en local)

## Installation
No need our server is host on heroku just head over https://discord.gg/ukfmUH5Q5e and start typing

## Available intents
| Inputs                                              | Output                                                | Example                         |
|-------------------------------------------------------|-------------------------------------------------------|---------------------------------|
|{Greetings}                                              | Hello! Do you want some information?                  | hi i'm new here                 |
|{Informations} or {help}                                           | this chatbot can recommand songs according to  artist genre and year. (use  recommend verb or his synonymes in english)  | can you give me help with the functionnality? |
|Recommendation  can you recommend me a song by {artist} from  {year} by {genre}  | a song from 1979 artist: KISS I Was Made For Lovin' You  | recommend a song from Kiss from 1979  |
|play {song} or {positions in output}                                           | if you want to play this song type precisely: music.play {song}                              | play Dance Monkey     |
|(If you are on a voice channel) music.play {song} |Enqueued {song} *play the song in the voice channel* |music.play I Want To Break Free
