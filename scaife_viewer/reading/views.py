from django.shortcuts import render, get_object_or_404

from account.decorators import login_required

from .models import metadata, recent, ReadingList


@login_required
def logs(request):
    reading_logs = request.user.readinglog_set.order_by("-timestamp")

    return render(request, "reading/logs.html", {
        "logs": reading_logs,
        "recent": recent(request.user),
    })


def reading_list(request, pk):
    lst = get_object_or_404(ReadingList, pk=pk)
    entries = [
        {
            "urn": entry.urn,
            **metadata(entry.urn),
        }
        for entry in lst.entries.all()
    ]
    return render(request, "reading/list_detail.html", {
        "reading_list": lst,
        "entries": entries,
    })
