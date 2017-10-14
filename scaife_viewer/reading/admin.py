from django.contrib import admin

from .models import ReadingLog, ReadingList, ReadingListEntry


@admin.register(ReadingLog)
class ReadingLogAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "urn", "timestamp"]


class ReadingListEntryInline(admin.TabularInline):
    model = ReadingListEntry


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner"]
    inlines = [ReadingListEntryInline]
