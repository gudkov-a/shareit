# shareit

The intent of this project is to store some information like URLs, texts and pictures for myself or someone else, like a personal bookmarks.

This is not the code I'm proud of. There are a lot of work need to be done and right now you should consider this only as an example not a complete product.

In this project I use:
 * Django 2.2
 * Pillow
 * JavaScript + JQuery
 * SQLite

What I did here:
* simple anti brute force auth backend
* user interface has a roulette which you can use to switch between bookmarks
* there are few commands on management folder that can be used as cron jobs to clean up old entries
* crucial parts of the code covered with tests
* there are different template for mobile users

How to run:
* clone the repo
* cd into the project dir and run ./initial.sh
* run development server: python3 manage.py runserver 0.0.0.0:8000