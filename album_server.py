#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

@route("/albums/<artist>")
def albums(artist):
	album_list = album.find(artist)
	if not album_list:
		message = "Альбомов {} не найдено".format(artist)
		result = HTTPError(404, message)
	else:
		album_names = [album.album for album in album_list]
		result = "Список альбомов {}: <br>".format(artist)
		result += "<br>".join(album_names)
	return result

@route("/albums", method="POST")
def create_album():
	year = request.forms.year
	artist = request.forms.artist
	genre = request.forms.genre
	album_name = request.forms.album

	try:
		year = int(year)
	except ValueError:
		return HTTPError(400, "Указан некорректный год альбома")

	try:
		new_album = album.save(year, artist, genre, album_name)
	except AssertionError as err:
		result = HTTPError(400, str(err))
	except album.AlreadyExists as err:
		result = HTTPError(409, str(err))
	else:
		print("New #{} album successfully saved".format(new_album.id))
		result = "Альбом #{} успешно сохранен".format(new_album.id)
		return result

if __name__ == "__main__":
	run(host="localhost", port=8080, debug=True)