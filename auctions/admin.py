from django.contrib import admin

# Register your models here.

from .models import User, Auction, Bid, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('username',)
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined',)

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'offerer', 'created', 'is_open')
    ordering = ('-created',)
    search_fields = ('name', 'category')
    list_filter = ('is_open', 'created',)

class BidAdmin(admin.ModelAdmin):
    list_display = ('for_auction', 'who_bid', 'created', 'bid')
    ordering = ('-created',)
    list_filter = ('for_auction', 'who_bid',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('for_auction', 'who_comment', 'created')
    ordering = ('-created',)
    list_filter = ('for_auction', 'who_comment', 'created',)

admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.site_header = "Auction Site Administration"
