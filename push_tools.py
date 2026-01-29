from typing import Any

import braintrust
from pydantic import BaseModel, RootModel

from catalog import MUSIC_CATALOG
from evals.core import PROJECT_NAME

project = braintrust.projects.create(name=PROJECT_NAME)


class SearchSongsParams(BaseModel):
    genre: str | None = None
    mood: str | None = None


class SongSummary(BaseModel):
    id: str
    title: str
    artist: str


class SearchSongsOutput(RootModel[list[SongSummary]]):
    pass


def search_songs(genre: str | None = None, mood: str | None = None) -> list[dict[str, Any]]:
    results = MUSIC_CATALOG
    if genre:
        results = [s for s in results if s["genre"].lower() == genre.lower()]
    if mood:
        results = [s for s in results if s["mood"].lower() == mood.lower()]
    return [{"id": s["id"], "title": s["title"], "artist": s["artist"]} for s in results]


project.tools.create(
    handler=search_songs,
    name="search_songs",
    slug="search_songs",
    description="Search for songs in the catalog by genre or mood.",
    parameters=SearchSongsParams,
    returns=SearchSongsOutput,
    if_exists="replace",
)


class GetSongDetailsParams(BaseModel):
    song_id: str


class SongDetails(BaseModel):
    id: str
    title: str
    artist: str
    genre: str
    mood: str
    duration_sec: int


class SongDetailsOutput(RootModel[SongDetails | None]):
    pass


def get_song_details(song_id: str) -> dict[str, Any] | None:
    for song in MUSIC_CATALOG:
        if song["id"] == song_id:
            return song
    return None


project.tools.create(
    handler=get_song_details,
    name="get_song_details",
    slug="get_song_details",
    description="Get detailed information about a specific song by ID.",
    parameters=GetSongDetailsParams,
    returns=SongDetailsOutput,
    if_exists="replace",
)


class CreatePlaylistParams(BaseModel):
    name: str
    song_ids: list[str]


class PlaylistSong(BaseModel):
    title: str
    artist: str


class PlaylistOutput(BaseModel):
    playlist_name: str
    songs: list[PlaylistSong]
    total_tracks: int
    total_duration_min: float


def create_playlist(name: str, song_ids: list[str]) -> dict[str, Any]:
    songs = []
    total_duration = 0
    for sid in song_ids:
        song = get_song_details(sid)
        if song:
            songs.append({"title": song["title"], "artist": song["artist"]})
            total_duration += song["duration_sec"]

    return {
        "playlist_name": name,
        "songs": songs,
        "total_tracks": len(songs),
        "total_duration_min": round(total_duration / 60, 1),
    }


project.tools.create(
    handler=create_playlist,
    name="create_playlist",
    slug="create_playlist",
    description="Create a playlist with the specified songs.",
    parameters=CreatePlaylistParams,
    returns=PlaylistOutput,
    if_exists="replace",
)
