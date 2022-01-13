from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from .models import User, Auction, Bid, Comment


#-------------------------- functions for module -------------------------

def commoncategories(auctions):
    auctions = auctions
    categories = []
    for auction in auctions:
        if auction.category in categories:
            continue
        else:
            categories.append(auction.category)
    categories.sort()
    return categories


def commonbids(auctions):
    auctions = auctions
    bids = Bid.objects.all()
    auctions_bids = {}
    for auction in auctions:
        bids_for_auction = []
        for bid in bids:
            if bid.for_auction_id == auction.id:
                bids_for_auction.append(bid)
        if bids_for_auction:
            auctions_bids.update({auction.id : bids_for_auction[len(bids_for_auction) - 1]})
    return auctions_bids


def actualbid(auction):
    bids = Bid.objects.filter(for_auction=auction.id)
    if bids:
        bid = bids[len(bids) - 1].bid
        who_bid = bids[len(bids) - 1].who_bid
    else:
        bid = 0
        who_bid = 'none__$&$&$&$@@&&never--$$$$$$$4nobody__ever$$$$$$@@@@@@@@@@&&&&&&&&&'
    return bid, who_bid


def watchlist(auction, current_user):
    follow = False
    followers = auction.follower.all()
    for follower in followers:
            if follower == current_user:
                follow = True
    return follow    


def new_bid(auction, bids, nbid, new, current_user):
    message = ''
    follow = False
    try:
        nbid.bid = Decimal(new)
    except:
        nbid.bid = 0
    if nbid.bid < auction.init_bid and not bids:
        message = 'Your bid must equal or greater than base bid'
    else:
        if bids and nbid.bid <= bids[len(bids) - 1].bid:
            message = 'Your bid must greater than last bid'
        else:
            nbid.who_bid = current_user
            nbid.for_auction = auction
            nbid.save()
            auction.follower.add(current_user)   
            follow = True     
    return message, follow



#------------------------- views -----------------------------#

# user area

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# listings display

def index(request):
    auctions = Auction.objects.filter(is_open='True')
    categories = commoncategories(auctions)
    auctions_bids = commonbids(auctions)
    message = 'Active Listings'
    message1 = 'No active Listings'
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "auctions_bids": auctions_bids,
        "categories": categories,
        "message": message,
        "message1": message1
        })


@login_required(login_url = "http://localhost:8000/login")
def listall(request):
    all_auctions = Auction.objects.all()
    auctions = Auction.objects.filter(is_open=True)
    message = 'All Listings'
    if all_auctions:
        categories = commoncategories(auctions)
        auctions_bids = commonbids(all_auctions)
        return render(request, "auctions/index.html", {
            "auctions": all_auctions,
            "auctions_bids": auctions_bids,
            "categories": categories,
            "message": message
            })
    else:
        message1 = 'No Listings'
        return render(request, "auctions/error.html", {
            "message": message,
            "message1": message1
            })


def allcategories(request):
    auctions = Auction.objects.filter(is_open=True)
    categories = commoncategories(auctions)
    return render(request, "auctions/allcategories.html", {
        "categories": categories
        })


def categories(request, category):
    active_auctions = Auction.objects.filter(is_open=True)
    categories = commoncategories(active_auctions)
    auctions = Auction.objects.filter(category=category, is_open=True)
    auctions_bids = commonbids(auctions)
    message1 = 'No Active Listings for this Category'
    return render(request, "auctions/index.html", {
        'message': category.capitalize(),
        "auctions": auctions,
        "auctions_bids": auctions_bids,
        "categories": categories,
        "message1": message1
        })


@login_required(login_url = "http://localhost:8000/login")
def following(request):
    all_auctions = Auction.objects.all()
    cat_auctions = Auction.objects.filter(is_open=True)
    message = 'Watchlist'
    categories = commoncategories(cat_auctions)
    follower = request.user
    auctions = Auction.objects.filter(follower=follower.id)
    if auctions:
        auctions_bids = commonbids(auctions)
        return render(request, "auctions/index.html", {
            "auctions": auctions,
            "auctions_bids": auctions_bids,
            "categories": categories,
            "message": message
            })
    else:
        message1 = 'No Listings for this Watchlist'
        return render(request, "auctions/error.html", {
            'message': message,
            'message1': message1
            })


@login_required(login_url = "http://localhost:8000/login")
def closedauctions(request):
    auctions = Auction.objects.filter(is_open=True)
    closauctions = Auction.objects.filter(is_open=False)
    categories = commoncategories(auctions)
    auctions_bids = commonbids(closauctions)
    message = "Closed Auctions"
    if closauctions:
        return render(request, "auctions/index.html", {
            "auctions": closauctions,
            "auctions_bids": auctions_bids,
            "categories": categories,
            'message': message
            })
    else:
        message1 = "No Auctions Closed"
        return render(request, "auctions/error.html", {
            'message': message,
            'message1': message1
            })


def auction(request, id):
    message = ''
    follow = False
    current_user = request.user
    exists_auction = Auction.objects.filter(id=id).exists()
    if exists_auction:
        auction = Auction.objects.get(id=id)
        follow = watchlist(auction, current_user)
        if request.method == "POST":
            bids = Bid.objects.filter(for_auction=id)
            nbid = Bid()
            new = request.POST['nbid']
            message, follow = new_bid(auction, bids, nbid, new, current_user)
        bid, who_bid = actualbid(auction)                    
        comments = Comment.objects.filter(for_auction=id)
        return render(request, 'auctions/auction.html', {
            'auction': auction,
            'who_bid': who_bid,
            'bid': bid,
            'message': message,
            'follow': follow,
            'comments': comments
        })
    else:
        message1 = 'The listing does not exist'
        return render(request, 'auctions/error.html', {
            'message1': message1
        })

# changes zone

@login_required(login_url = "http://localhost:8000/login")
def newauction(request):
    if request.method == "POST":
        auction = Auction()
        auction.name = request.POST["name"]
        if auction.name == '':
            auction.name = 'Nameless'
        auction.category = (request.POST["category"]).lower()
        if auction.category == '':
            auction.category = 'uncategorized'
        auction.description = request.POST["description"]
        if auction.description == '':
            auction.description = 'No description'
        try:
            max_value = 9999999.99
            auction.init_bid = abs(Decimal(request.POST["init_bid"]))
            if auction.init_bid == 0.00 or auction.init_bid > max_value:
                auction.init_bid = 0.01
        except:
            auction.init_bid = 0.01
        auction.image = request.FILES.get("image", "null")
        auction.offerer = request.user
        auction.save()
        auction.follower.add(request.user)
        return HttpResponseRedirect(reverse("auction", args=[auction.id]))
    else:
        return render(request, "auctions/newauction.html")


@login_required(login_url = "http://localhost:8000/login")
def close(request):
    status_id = request.GET['close']
    auction = Auction.objects.get(id=status_id)
    auction.is_open = False
    auction.save()
    return HttpResponseRedirect(reverse("auction", args=[status_id]))


@login_required(login_url = "http://localhost:8000/login")
def delivered(request):
    status_id = request.GET['delivered']
    auction = Auction.objects.get(id=status_id)
    auction.delivered = True
    auction.save()
    return HttpResponseRedirect(reverse("auction", args=[status_id]))


@login_required(login_url = "http://localhost:8000/login")
def deleted(request):
    if request.method == "GET":
        status_id = request.GET['del']
        auction = Auction.objects.get(id=status_id)
        auction.delete()
        message1 = 'The listing was successfully deleted'
    else:
        message1 = 'Page not found'
    return render(request, 'auctions/error.html', {
        'message1': message1
    })


@login_required(login_url = "http://localhost:8000/login")
def followadd(request):
    follower = request.user
    f_id = request.GET['followes']
    auction = Auction.objects.get(id=f_id)
    auction.follower.add(follower)
    return HttpResponseRedirect(reverse("auction", args=[f_id]))

@login_required(login_url = "http://localhost:8000/login")
def followremove(request):
    follower = request.user
    f_id = request.GET['followrem']
    auction = Auction.objects.get(id=f_id)
    auction.follower.remove(follower)
    return HttpResponseRedirect(reverse("auction", args=[f_id]))


@login_required(login_url = "http://localhost:8000/login")
def newcomment(request):
    if request.method == "POST":
        n_id = request.POST['new']
        comm = Comment()
        auction = Auction.objects.get(id=n_id)
        comm.comment = request.POST['newcommen']
        if comm.comment != '':
            comm.for_auction = auction
            comm.who_comment = request.user
            comm.save()
        else:
            pass
        return HttpResponseRedirect(reverse("auction", args=[n_id]))


def error(request):
    return render(request, 'auctions/error.html')
