from django.contrib import admin
from .models import Location, Gym, Review, Like, GymImage, ReviewImage

class GymImageInline(admin.TabularInline):
    model = GymImage
    extra = 4

class GymAdmin(admin.ModelAdmin):
    inlines = [GymImageInline]

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageInline]

admin.site.register(Location)
admin.site.register(Gym, GymAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Like)
# admin.site.register(GymImage)
# admin.site.register(ReviewImage)
