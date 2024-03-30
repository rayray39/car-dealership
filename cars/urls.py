from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login_view"),    # /log_in
    path("logout", views.logout_view, name="logout_view"), # /log_out
    path("register", views.register, name="register"),  # /register
    path("", views.index, name="index"),    # /  (this is the default url path)

    path("create_new_listing", views.create_new_listing, name="create_new_listing"),  # /create_new_listing
    path("car_listing/<int:listing_id>", views.car_listing, name="car_listing"),     # /car_listing/id

    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),  # /place_bid/id, function to place bid

    path("make_comment/<int:listing_id>", views.make_comment, name="make_comment"), # /make_comment/id

    path("categories", views.categories, name="categories"),
    path("category/<str:selected_category>", views.category, name="category"),

    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),

    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
]